import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')  # Import secret key from .env
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """
    This is the configuration class for our dev environment
    """
    DEBUG = config('DEBUG', True, cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite')


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
