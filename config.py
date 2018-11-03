import logging
from werkzeug.routing import BaseConverter

class Config(object):
    # 通过mongoengine连接mongodb的配置信息
    MONGODB_SETTINGS = {
    'db': 'scrapydb',
    'host': '127.0.0.1',
    'port': 27017,
    'username': 'cino',
    'password': 'cino',
    }

    # 通过pymongo直接连接mongodb的配置信息
    MONGO_AUTH = 'mongodb://cino:cino@127.0.0.1/scrapydb'


class DevelepmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

config_dict = {'develepment': DevelepmentConfig,
          'production': ProductionConfig}