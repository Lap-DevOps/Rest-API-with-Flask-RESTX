from decouple import config


class Config(object):
    SECRET_KEY = config('SECRET_KEY', default='secret-key')


class DevConfig(Config):
    DEBUG = config('DEBUG', default=True, cast=bool)


class TestConfig(Config):
    TESTING = config('TESTING', default=True, cast=bool)


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}