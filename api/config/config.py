import os.path
from datetime import timedelta

from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = config('SECRET_KEY', default='secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='secret-key')


class DevConfig(Config):
    DEBUG = config('DEBUG', default=True, cast=bool)
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI',
                                     default='sqlite:///database.db')
    SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', default=True, cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    TESTING = config('TESTING', default=True, cast=bool)
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
