import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_mongoengine import MongoEngine

from config import config_dict, RegexConverter

mongodb = MongoEngine()
def create_log(config_name):
    """记录日志的配置信息"""
    # 设置日志的记录等级
    # config_dict[config_name].LOG_LEVEL 获取配置类中对象日志的级别
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=2)

    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    # INFO manage.py: 18 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def create_app(config_name):
    # 开启日志
    create_log(config_name)
    # 创建app对象
    app = Flask(__name__)
    # 配置信息
    config_class = config_dict[config_name]
    app.config.from_object(config_class)
    # 自定义正则转换器
    app.url_map.converters['re'] = RegexConverter

    # 加载数据库对象
    mongodb.init_app(app)

    from apps.recruit import recruit_bp
    app.register_blueprint(recruit_bp)

    return app