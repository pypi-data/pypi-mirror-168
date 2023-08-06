from nubium_utils.confluent_utils.producer_utils import get_producers
from nubium_utils.confluent_utils.confluent_configs import init_schema_registry_configs, env_vars
from nubium_utils.yaml_parser import load_yaml_fp


def gtfo_producer(topic_schema_dict):
    """
    This assumes all produce topics are on the same cluster, too lazy to add a check for now
    """
    cluster_name = load_yaml_fp(env_vars()['NU_TOPIC_CONFIGS_YAML'])[list(topic_schema_dict.keys())[0]]['cluster']
    return get_producers(topic_schema_dict, cluster_name, init_schema_registry_configs())
