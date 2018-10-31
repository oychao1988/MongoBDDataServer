from flask import current_app, jsonify
from flask import request
from flask import views

from models import FingerPrint
from utils import constants
from utils.response_code import RET
from . import recruit_bp


# /duplicateChecking 数据库查重
class DuplicateCheckingView(views.MethodView):
    # GET查询指纹
    def get(self):
        """
        number: CC237101814J00144096106
        updateDate: 2018-10-19 18:08:21
        :return:
        """
        try:
            number = int(request.args.get('number'))
            updateDate = int(request.args.get('updateDate'))
            source = request.args.get('source')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, source, updateDate]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerprint = FingerPrint.objects(number=number, source=source).first()
        if fingerprint:
            data = {
                'number': fingerprint.number,
                'updateDate': fingerprint.updateDate,
                'source': fingerprint.source
            }
            # 比较更新日期
            if updateDate > fingerprint['updateDate']:
                return jsonify(errno=RET.UPDATE, errmsg='数据可更新', data=data)
            else:
                return jsonify(errno=RET.OK, errmsg='数据已存在', data=data)
        else:
            return jsonify(errno=RET.NODATA, errmsg='无数据')

    # POST保存指纹
    def post(self):
        try:
            number = int(request.form.get('number'))
            updateDate = int(request.form.get('updateDate'))
            source = request.form.get('source')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate, source]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        try:
            fingerprint = FingerPrint(number=number, updateDate=updateDate, source=source).save()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据保存错误')
        # 组织返回数据
        data = {  # 'id': fingerprint.id, # TODO 如何返回ID
            'number': fingerprint.number,
            'updateDate': fingerprint.updateDate,
            'source': fingerprint.source}

        return jsonify(errno=RET.OK, errmsg='数据提交成功', data=data)

    # PUT修改指纹
    def put(self):
        try:
            number = int(request.args.get('number'))
            updateDate = int(request.args.get('updateDate'))
            source = request.args.get('source')
            # updateDate = datetime.strptime(updateDate, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate, source]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')
        fingerprint = FingerPrint.objects(number=number, source=source).first()
        if not fingerprint:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        # 更新数据
        fingerprint.update(updateDate=updateDate)
        # 组织返回数据
        fingerprint = FingerPrint.objects(number=number).first()
        data = {  # 'id': fingerprint.id, # TODO 如何返回ID
            'number': fingerprint.number,
            'updateDate': fingerprint.updateDate,
            'source': fingerprint.source}
        return jsonify(errno=RET.OK, errmsg='成功', data=data)

    # DELETE删除指纹
    def delete(self):
        try:
            number = int(request.args.get('number'))
            source = request.args.get('source')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not [number, source]:
            jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerPrint = FingerPrint.objects(number=number, source=source).first()
        if not fingerPrint:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        fingerPrint.delete()
        return jsonify(errno=RET.OK, errmsg='OK')

class BaseRecruitDataView(views.MethodView):
    COLLECTION = None # 集合模型类

    # 查询职位信息
    def get(self, positionId):
        args = {k: v for k, v in request.args.items()}
        # 单个数据
        if positionId:
            # 禁止添加查询字符串
            if args:
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
            # 参数验证
            try:
                positionId = int(positionId)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

            position_data = self.COLLECTION.objects(positionId=positionId).first()
            if not position_data:
                return jsonify(errno=RET.NODATA, errmsg='数据不存在')
            return jsonify(errno=RET.OK, errmsg='OK', data=position_data.to_dict())

        # 多个数据
        else:
            # 控制参数范围
            args_keys = [k for k in args]
            allow_args = [[], ['page'], ['per_page'], ['page', 'per_page']]
            if args_keys not in allow_args:
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
            try:
                page = request.args.get('page', 1)
                per_page = request.args.get('per_page', constants.PER_PAGE_MAX_NUM)
                page = int(page)
                per_page = int(per_page)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

            paginate = self.COLLECTION.objects.paginate(page=page, per_page=per_page)
            items = paginate.items
            total_page = paginate.pages
            current_page = paginate.page
            recruit_data = {
                'recruits_list': items,
                'current_page': current_page,
                'total_page': total_page
            }
            return jsonify(errno=RET.OK, errmsg='查询招聘信息列表', data=recruit_data)

    # 增加职位信息
    def post(self, positionId):
        # 获取参数
        data_dict = {k: str(v) for k, v in request.form.items()}
        # 保存数据
        try:
            collection = self.COLLECTION(**data_dict).save()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据保存错误')
        # 返回结果
        return jsonify(errno=RET.OK, errmsg='数据保存成功', data=collection.to_dict())

    # 更新职位信息
    def put(self, positionId):
        # 参数验证
        try:
            positionId = int(positionId)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        position_data = self.COLLECTION.objects(positionId=positionId).first()
        if not position_data:
            return jsonify(errno=RET.NODATA, errmsg='无数据')

        # 获取参数
        data_dict = {k: str(v) for k, v in request.form.items()}
        # 保存数据
        try:
            position_data.update(**data_dict)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据保存错误')
        position_data = self.COLLECTION.objects(positionId=positionId).first()
        return jsonify(errno=RET.OK, errmsg='OK', data=position_data.to_dict())

    # 删除职位信息
    def delete(self, positionId):
        try:
            positionId = str(positionId)
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        position_data = self.COLLECTION.objects(positionId=positionId).first()
        if not position_data:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        position_data.delete()
        return jsonify(errno=RET.OK, errmsg='OK')

# /lagou 拉勾招聘信息数据视图
class LagouRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').LagouData

# /zhilian 智联招聘信息数据视图
class ZhilianRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').ZhilianData

# /liepin 猎聘招聘信息数据视图
class LiepinRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').LiepinData

# /51job 51job招聘信息数据视图
class Job51RecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').Job51Data

# /zhipin BOSS直聘招聘信息数据视图
class ZhipinRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').ZhipinData

# 查重视图
recruit_bp.add_url_rule('/duplicateChecking', view_func=DuplicateCheckingView.as_view('duplicateCheckingView'))
# lagou招聘信息试图路由
recruit_bp.add_url_rule('/lagou/', view_func=LagouRecruitDataView.as_view('lagous'), defaults={'positionId': None})
recruit_bp.add_url_rule('/lagou/<int:positionId>', view_func=LagouRecruitDataView.as_view('lagou'),
                        methods=['GET', 'PUT', 'DELETE'])
# /zhilian 智联招聘信息试图路由
recruit_bp.add_url_rule('/zhilian/', view_func=ZhilianRecruitDataView.as_view('zhilians'), defaults={'positionId': None})
recruit_bp.add_url_rule('/zhilian/<int:positionId>', view_func=ZhilianRecruitDataView.as_view('zhilian'),
                        methods=['GET', 'PUT', 'DELETE'])
# /liepin 猎聘招聘信息试图路由
recruit_bp.add_url_rule('/liepin/', view_func=ZhilianRecruitDataView.as_view('liepins'), defaults={'positionId': None})
recruit_bp.add_url_rule('/liepin/<int:positionId>', view_func=ZhilianRecruitDataView.as_view('liepin'),
                        methods=['GET', 'PUT', 'DELETE'])
# /51job 51job招聘信息试图路由
recruit_bp.add_url_rule('/51job/', view_func=ZhilianRecruitDataView.as_view('51jobs'), defaults={'positionId': None})
recruit_bp.add_url_rule('/51job/<int:positionId>', view_func=ZhilianRecruitDataView.as_view('51job'),
                        methods=['GET', 'PUT', 'DELETE'])
# /zhipin BOSS直聘招聘信息试图路由
recruit_bp.add_url_rule('/zhipin/', view_func=ZhilianRecruitDataView.as_view('zhipins'), defaults={'positionId': None})
recruit_bp.add_url_rule('/zhipin/<int:positionId>', view_func=ZhilianRecruitDataView.as_view('zhipin'),
                        methods=['GET', 'PUT', 'DELETE'])