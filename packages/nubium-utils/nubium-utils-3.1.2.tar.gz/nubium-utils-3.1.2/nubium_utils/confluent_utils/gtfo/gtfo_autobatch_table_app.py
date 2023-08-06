from .gtfo_table_app import GtfoTableApp, TableTransaction
from .gtfo_app import NoMessageError, KafkaException, handle_kafka_exception
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from confluent_kafka import TopicPartition
import logging
from copy import deepcopy
from datetime import datetime


LOGGER = logging.getLogger(__name__)


class AutoBatchTableTransaction(TableTransaction):
    def __init__(self, producer, consumer, app_changelog_topic, app_tables, metrics_manager=None, message=None, auto_consume=True, timeout=5, parent_app=None):
        self._commit_offsets = {}
        self.message_count = 0
        super().__init__(producer, consumer, app_changelog_topic=app_changelog_topic, app_tables=app_tables, metrics_manager=metrics_manager, message=message, auto_consume=auto_consume, timeout=timeout, parent_app=parent_app)

    def _refresh_transaction_fields(self):
        super()._refresh_transaction_fields()
        self._commit_offsets = {}
        self.message_count = 0

    def read_table_entry(self):
        pending_update = self._pending_table_writes.get(self.partition(), {}).get(self.key())
        if pending_update:
            return deepcopy(pending_update)
        return super().read_table_entry()

    def consume(self):
        super().consume()
        self._commit_offsets[self.partition()] = {"topic": self.topic(), "partition": self.partition(), "offset": self.offset()}
        self.message_count += 1

    def commit(self, mark_committed=True):
        # TODO: Confirm there aren't commits from old partition assignments (not sure how that's handled...it may not rebalance
        #  while doing a transaction?)
        try:
            LOGGER.info('Committing Transaction...')
            offsets_to_commit = [TopicPartition(msg['topic'], msg['partition'], msg['offset'] + 1) for msg in
                                 self._commit_offsets.values()]
            if offsets_to_commit:
                LOGGER.debug(f'Offsets to commit: {offsets_to_commit}')
                self._init_transaction()
            if self._active_transaction:
                LOGGER.info(f'Committing {self.message_count} messages...')
                self.producer.send_offsets_to_transaction(offsets_to_commit, self.consumer.consumer_group_metadata())
                self.producer.commit_transaction(30)
                self.producer.poll(0)  # TODO: experiment with flushing? I think it does it by default
                LOGGER.info('All partition transactions committed!')
                self._committed = mark_committed
                self._commit_offsets = {}
                self.message_count = 0
                self._retry_offsets = {}
                if self._committed:
                    self._active_transaction = False
            self._table_write()
        except KafkaException as kafka_error:
            handle_kafka_exception(kafka_error)


class GtfoAutoBatchTableApp(GtfoTableApp):
    def __init__(self, app_function, consume_topic, produce_topic_schema_dict=None, transaction_type=AutoBatchTableTransaction,
                 app_function_arglist=None, metrics_manager=None, schema_registry=None, cluster_name=None, consumer=None, producer=None,
                 time_elapse_max_seconds=None, consume_max_count=None):

        self._time_elapse_start = None

        if time_elapse_max_seconds is None:
            time_elapse_max_seconds = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_TIME_SECONDS'])
        if consume_max_count is None:
            consume_max_count = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_COUNT'])

        self._time_elapse_max_seconds = time_elapse_max_seconds
        self._consume_max_count = consume_max_count

        super().__init__(
            app_function, consume_topic, produce_topic_schema_dict, transaction_type=transaction_type,
            app_function_arglist=app_function_arglist, metrics_manager=metrics_manager, schema_registry=schema_registry, cluster_name=cluster_name, consumer=consumer, producer=producer)

    def prepare_transaction(self, *args, **kwargs):
        return super().consume(*args, auto_consume=False, **kwargs)

    def _max_consume_time_continue(self):
        if self._time_elapse_max_seconds:
            seconds_elapsed = datetime.now().timestamp() - self._time_elapse_start
            return seconds_elapsed < self._time_elapse_max_seconds
        return True

    def _max_consume_count_continue(self, consume_multiplier=1):
        if self._consume_max_count:
            return self.transaction.message_count < (self._consume_max_count * consume_multiplier)
        return True

    def _keep_consuming(self, consume_multiplier=None):
        if not consume_multiplier:
            consume_multiplier = 1
        return not self._shutdown and self._max_consume_count_continue(consume_multiplier=consume_multiplier) and self._max_consume_time_continue()

    def _check_pending_recovery_status(self):
        recovery_elapsed_time = int(datetime.timestamp(datetime.now())) - self._recovery_time_start
        LOGGER.debug(f'Current pending recovery partition statuses before refreshing: {self._pending_table_recoveries}')
        recovery_status = {p: {'table_offset': self.transaction._table_offset(partition=p), 'highwater': self._pending_table_recoveries[p]['watermarks'][1]} for p in self._pending_table_recoveries.keys()}
        current_recovery_offsets_remaining = {p: recovery_status[p]['highwater'] - recovery_status[p]['table_offset'] for p in recovery_status}
        total_remaining_offsets = sum(current_recovery_offsets_remaining.values())
        offsets_processed = self._recovery_offsets_remaining - total_remaining_offsets
        self._recovery_offsets_handled += offsets_processed
        self._recovery_offsets_remaining = total_remaining_offsets
        recovery_rate_offsets_sec = self._recovery_offsets_handled / recovery_elapsed_time
        remaining_time_mins = round((self._recovery_offsets_remaining / recovery_rate_offsets_sec) / 60, 2)
        LOGGER.debug(f'RECOVERY - offsets processed this iteration: {offsets_processed}')
        LOGGER.debug(f'RECOVERY - current process rate: {int(recovery_rate_offsets_sec)} offsets/sec')
        LOGGER.info(f'RECOVERY - {self._recovery_offsets_handled} TOTAL OFFSETS PROCESSED OVER {round(recovery_elapsed_time / 60, 2)} minutes')
        LOGGER.info(f'RECOVERY - ESTIMATED TIME REMAINING: {remaining_time_mins} minutes')
        LOGGER.info(f'RECOVERY - OFFSETS REMAINING: {current_recovery_offsets_remaining}')
        for p in recovery_status:
            if recovery_status[p]['highwater'] - (recovery_status[p]['table_offset'] + 2) <= 0:  # +2 comes from: +1 due to table tracking offset it has up to, and another +1 due to last offset expecting to be a transaction marker
                LOGGER.info(f'Offset delta for p{p} is within an expected tolerable range of the changelog highwater; it is safe to assume transactional markers are the remaining delta.')
                self._set_table_offset_to_latest(p)

    def _table_recovery_loop(self, checks=2, consume_multiplier=10):
        while self._pending_table_recoveries and checks:
            LOGGER.info(f'Consuming from changelog partitions: {list(self._active_table_changelog_partitions.keys())}')
            self.prepare_transaction()
            if self._time_elapse_max_seconds:
                self._time_elapse_start = datetime.now().timestamp()
            LOGGER.info(f'Processing up to {self._consume_max_count * consume_multiplier} messages for up to {self._time_elapse_max_seconds} seconds!')
            # NOTE: no transaction commits since its just consuming from changelog and writing to the table, we dont care about the consumer group offset
            try:
                while self._keep_consuming(consume_multiplier=consume_multiplier) and self._pending_table_recoveries and checks:
                    self.transaction.consume()
                    self.transaction._update_table_entry_from_changelog()
            except NoMessageError:  # NOTE: this does not necc mean no messages were pulled at all in the batch, just that there's now none left!
                checks -= 1
                LOGGER.debug(f'No further changelog messages, checks remaining: {checks}')
            LOGGER.info(f'Consumed {self.transaction.message_count} changelog messages')
            self.transaction._table_write(recovery_multiplier=consume_multiplier)  # relay transaction's cached writes to the table's write cache
            self._check_pending_recovery_status()
        self.commit_tables()
        self._check_pending_recovery_status()
        if not checks:
            for p in list(self._pending_table_recoveries.keys()):  # list stops dict iter size change exception
                self._set_table_offset_to_latest(p)

    def _app_run(self, *args, **kwargs):
        LOGGER.info(f'Consuming from partitions: {list(self._active_primary_partitions.keys())}')
        self.prepare_transaction(*args, **kwargs)
        if self._time_elapse_max_seconds:
            self._time_elapse_start = datetime.now().timestamp()
        LOGGER.info(
            f'Processing up to {self._consume_max_count} messages for up to {self._time_elapse_max_seconds} seconds!')
        try:
            while self._keep_consuming():
                self.transaction.consume()
                self.app_function(self.transaction, *self.app_function_arglist)
        except NoMessageError:
            self.producer.poll(0)
            LOGGER.info('No messages!')
        if any(self.transaction._pending_table_offset_increase.values()) or self.transaction._commit_offsets:
            self.transaction.commit()
            self.check_table_commits()
        else:
            self.commit_tables()
