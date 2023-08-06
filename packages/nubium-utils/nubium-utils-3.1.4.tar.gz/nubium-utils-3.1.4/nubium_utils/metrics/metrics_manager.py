"""
Container for standardized application monitoring gauges
"""
from prometheus_client import Gauge, CollectorRegistry
from nubium_utils.general_runtime_vars import env_vars
from nubium_utils.metrics.metrics_pusher import MetricsPusher


class Metric:
    def __init__(self, metric_name, registry, description='', job=None, app=None, additional_labels=None):
        if not job:
            job = env_vars()['NU_HOSTNAME']
        if not app:
            app = env_vars()['NU_APP_NAME']
        if not additional_labels:
            additional_labels = []

        self.name = metric_name
        self.app = app
        self.job = job
        self.additional_labels = list(sorted(additional_labels))
        self.all_labels = ['app', 'job'] + self.additional_labels
        self.store = Gauge(self.name, description, labelnames=self.all_labels, registry=registry)

    def _labels(self, label_dict):
        if not self.additional_labels:
            label_dict = {}
        return self.store.labels(self.app, self.job, *[i[1] for i in sorted(label_dict.items())])

    def inc(self, number=1, label_dict=None):
        self._labels(label_dict).inc(number)

    def set(self, number, label_dict=None):
        self._labels(label_dict).set(number)


class MetricsManager:
    """
    Coordinates Prometheus monitoring for a Kafka client application

    Creates and manages Metric instances and pushes their metrics
    """

    def __init__(self, registry=None, metrics_pusher: MetricsPusher = None):
        """
        Initializes monitor and Metric classes
        """
        if not metrics_pusher:
            metrics_pusher = MetricsPusher()
        if not registry:
            registry = CollectorRegistry()

        self.metrics_pusher = metrics_pusher
        self.registry = registry
        self._metrics = {}

        self.new_metric('messages_consumed', description='Messages consumed since application start', additional_labels=['topic']),
        self.new_metric('messages_produced', description='Messages produced since application start', additional_labels=['topic']),
        self.new_metric('message_errors', description='Exceptions caught when processing messages', additional_labels=['exception']),
        self.new_metric('external_requests', description='Network calls to external services', additional_labels=['request_to', 'request_endpoint', 'request_type', 'is_bulk', 'status_code']),
        self.new_metric('seconds_behind', description='Elapsed time since the consumed message was originally produced')

    def __getattr__(self, name):
        try:
            return self._metrics[name]
        except:
            return super().__getattribute__(name)

    @property
    def metric_names(self):
        return [metric.name for metric in self._metrics.values()]

    def new_metric(self, metric_name, description='', additional_labels=None):
        self._metrics[metric_name] = Metric(metric_name, self.registry, description=description, additional_labels=additional_labels)

    def inc_metric(self, metric_name, number=1, label_dict=None):
        self._metrics[metric_name].inc(number=number, label_dict=label_dict)

    def set_metric(self, metric_name, number, label_dict=None):
        self._metrics[metric_name].set(number, label_dict=label_dict)

    def push_metrics(self):
        self.metrics_pusher.set_metrics_pod_ips()
        self.metrics_pusher.push_metrics(self.registry)

    # ------------------------------- BELOW: BACKWARDS COMPATABILITY; remove in v4.0? --------------------------------

    def register_custom_metric(self, name, description):
        """ Register a custom metric to be used with inc_custom_metric later. """
        self.new_metric(name, description=description)

    def inc_custom_metric(self, name, amount=1):
        """
        Increases a registered custom metric by the amount specified (defaults to 1).

        `name`'s value must be registered in advance by calling register_custom_metric.
        """
        if name not in self._metrics:
            raise ValueError(f"'{name}' was not registered via register_custom_metric.")
        self.inc_metric(name, number=amount)

    def inc_messages_consumed(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.inc_metric('messages_consumed', number=number_of_messages, label_dict={'topic': topic})

    def inc_messages_produced(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.inc_metric('messages_produced', number=number_of_messages, label_dict={'topic': topic})

    def inc_message_errors(self, exception):
        """
        Increases the error gauge with default label and label of the exception
        """
        self.inc_metric('message_errors', label_dict={'exception': exception.__class__.__name__})

    def inc_external_requests(self, request_to=None, request_endpoint=None, request_type=None, is_bulk=0, status_code=200):
        """
        Increases the external requests gauge.
        """
        self.inc_metric(
            'external_requests',
            label_dict={
                "request_to": request_to,
                "request_endpoint": request_endpoint,
                "request_type": request_type,
                "is_bulk": is_bulk,
                "status_code": status_code})

    def set_seconds_behind(self, seconds_behind):
        """
        Sets the seconds_behind gauge with default labels
        """
        self.set_metric('seconds_behind', seconds_behind)
