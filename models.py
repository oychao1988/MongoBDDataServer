from pymongo import MongoClient

from apps import mongodb
from config import Config

MONGO_CLIENT = MongoClient(Config.MONGO_AUTH)

LagouClient = MONGO_CLIENT['scrapydb']['lagouRecruit']
ZhilianClient = MONGO_CLIENT['scrapydb']['zhilianRecruit']
LiepinClient = MONGO_CLIENT['scrapydb']['liepinRecruit']
Job51Client = MONGO_CLIENT['scrapydb']['job51Recruit']
ZhipinClient = MONGO_CLIENT['scrapydb']['zhipinRecruit']


# 指纹集合
class FingerPrint(mongodb.Document):
    meta = {
        'collection': 'fingerPrint'
    }
    number = mongodb.IntField()
    updateDate = mongodb.IntField()
    source = mongodb.StringField()


"""
# 拉勾招聘信息
class LagouData(mongodb.Document):
    # 指定集合名称
    meta = {'collection': 'lagouRecruit',
            'ordering': ['-createTime'],
            'strict': False,
            }
"""