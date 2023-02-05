import os
from decouple import config


class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')  # Import secret key from .env


class DevConfig(Config):
    """
    This is the configuration class for our dev environment
    """
    DEBUG = config('DEBUG', True, cast=bool)


class TestConfig(Config):
    """
    This handles the configuration files when we want to test our code
    """
    pass


class ProdConfig(Config):
    """
    This is the config class for production environment
    """
    pass


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}
