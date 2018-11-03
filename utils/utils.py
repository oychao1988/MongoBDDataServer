# /duplicateChecking 数据库查重
from flask import current_app

from models import FingerPrint


# 指纹查询对象
class FP():
    def __init__(self, number, source, updateDate=None):
        self.number = int(number)
        self.source = source
        if updateDate:
            self.updateDate = int(updateDate)
        self.exists = self._check

    # check查询指纹是否存在
    @property
    def _check(self):
        fp = FingerPrint.objects(number=self.number, source=self.source).first()
        if fp:
            if self.updateDate == fp.updateDate:
                return 1
            return -1
        else:
            return 0

    # create保存指纹
    def create(self):
        if not self.updateDate:
            current_app.logger.error('要创建的指纹对象updateDate字段为空')
            return False
        try:
            assert int(self.updateDate)
            FingerPrint(number=self.number, updateDate=self.updateDate, source=self.source).save()
        except Exception as e:
            current_app.logger.error(e)
            return False
        return True

    # update修改指纹
    def update(self):
        fingerprint = FingerPrint.objects(number=self.number, source=self.source).first()
        if not self.updateDate:
            current_app.logger.error('要更新的指纹对象updateDate字段为空')
            return False
        try:
            assert int(self.updateDate)
            fingerprint.update(updateDate=self.updateDate)
        except Exception as e:
            current_app.logger.error(e)
            return False
        return True


    # DELETE删除指纹
    def delete(self):
        fingerPrint = FingerPrint.objects(number=self.number, source=self.source).first()
        try:
            fingerPrint.delete()
        except Exception as e:
            current_app.logger.error(e)
            return False
        return True


def save(data_dict, COLLECTION, update=True):
    fp = FP(number=data_dict['positionId'],
            source=data_dict['source'],
            updateDate=data_dict['updateDate'])
    # 如果重复，则跳过该信息
    if fp.exists == 0: # 数据不存在
        try:
            # 添加指纹
            fp.create()
            del data_dict['source']
            # 向集合插入数据
            COLLECTION.insert_one(data_dict)
            # 获取数据用于返回
            data_dict = COLLECTION.find_one({'positionId':data_dict['positionId']})
            del data_dict['_id']
            return data_dict
        except Exception as e:
            fp.delete()
            current_app.logger.error(e)
            return False
    else:
        if fp.exists == 1: # 数据已存在，且已是最新
            return False
        if update and (fp.exists == -1): # 数据已存在，但可以更新
            del data_dict['source']
            # 更新指纹
            fp.update()
            # 更新数据
            COLLECTION.update({'positionId': data_dict['positionId']}, data_dict)
            data_dict = COLLECTION.find_one({'positionId':data_dict['positionId']})
            del data_dict['_id']
            return data_dict
        else:
            return False