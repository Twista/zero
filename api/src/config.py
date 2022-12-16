import logging
import os
from typing import Dict, Type


def _raise(ex):
    raise ex


def _minutes_to_seconds(mins: int):
    return mins * 60


class Config:
    SERVICE_NAME = "API"
    ENV = "@dev"
    LOGGING_LEVEL = logging.INFO
    WS_API = "http://localhost:3001/"
    IS_OFFLINE = os.environ.get("IS_OFFLINE")

    LAMBDA_PREFIX = f"{os.environ.get('APP_NAME')}-{os.environ.get('APP_ENV')}-"


###
# Local and Test ENV config
###

class LocalDev(Config):
    LOGGING_LEVEL = logging.DEBUG
    WS_API = os.environ.get("API_URL")


class TestingConfig(LocalDev):
    ENV = "@testing"


###
# ENV Configurations
###


class ProductionConfig(Config):
    ENV = "PRODUCTION"
    LOGGING_LEVEL = logging.INFO
    WS_API = os.environ.get("API_URL")


config_map: Dict[str, Type[Config]] = {
    'dev': LocalDev,
    'local': LocalDev,
    'testing': TestingConfig,
    'production': ProductionConfig
}

current_config: Type[Config] = config_map.get(os.environ.get('APP_ENV') or 'local')
