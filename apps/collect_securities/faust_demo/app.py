import faust

from config import config as main_config


def get_app():
    return faust.App("securities", broker=main_config.KAFKA_BROKERS)


app = get_app()
