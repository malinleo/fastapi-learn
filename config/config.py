from functools import partial, partialmethod
import os

from sitri import Sitri
from sitri.providers.contrib.system import SystemConfigProvider
from sitri.providers.contrib.yaml import YamlConfigProvider
from sitri.strategy.index_priority import IndexPriorityStrategy
from sitri.configurator import SitriProviderConfigurator

config_providers = (
    SystemConfigProvider(prefix="horton"),
    YamlConfigProvider(
        yaml_path=os.path.join(os.getcwd(), "config/config.yml"),
        default_separator="_",
    ),
)

configurator: SitriProviderConfigurator = Sitri(
    config_provider=IndexPriorityStrategy(*config_providers),
)

get_config = partial(configurator.get, path_mode=True)

KAFKA_BROKERS = get_config("kafka_servers")

MONGO_DATABASE_URI = "mongodb://{username}:{password}@{host}:{port}"
MONGO_DATABASE_NAME = get_config("mongo_database")
MONGO_DATABASE_USERNAME = get_config("mongo_username")
MONGO_DATABASE_PASSWORD = get_config("mongo_password")
MONGO_DATABASE_HOST = get_config("mongo_host")
MONGO_DATABASE_PORT = get_config("mongo_port")

MONGO_DATABASE_URI_WITH_AUTH = MONGO_DATABASE_URI.format(
    username=MONGO_DATABASE_USERNAME,
    password=MONGO_DATABASE_PASSWORD,
    host=MONGO_DATABASE_HOST,
    port=MONGO_DATABASE_PORT,
)

API_ENDPOINT = get_config("service_apiendpoint")
API_KEY = get_config("service_apikey")
