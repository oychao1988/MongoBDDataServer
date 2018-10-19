import logging

class Config(object):
    MONGODB_SETTINGS = {
    'db': 'scrapydb',
    'host': '127.0.0.1',
    'port': 27017,
    'username': 'cino',
    'password': 'cino',
    }


class DevelepmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


config_dict = {'develepment': DevelepmentConfig,
          'production': ProductionConfig}