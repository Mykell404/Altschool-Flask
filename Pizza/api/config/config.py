import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')  # Import secret key from .env file
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=4)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'secret') # Import secret key from .env file


class DevConfig(Config):
    """
    This is the configuration class for our dev environment
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')


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
