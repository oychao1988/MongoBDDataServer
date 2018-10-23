from flask import current_app, jsonify
from flask import request
from flask import views

from models import FingerPrint, LagouData
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
            number = request.args.get('number')
            source = request.args.get('source')
            # timestamp = datetime.timestamp(updateDate)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, source]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerprint = FingerPrint.objects(number=number, source=source).first()
        if fingerprint:
            data = {  # 'id': fingerprint.id, # TODO 如何返回ID
                'number': fingerprint.number,
                'updateDate': fingerprint.updateDate,
                'source': fingerprint.source
            }
            return jsonify(errno=RET.OK, errmsg='OK', data=data)
        else:
            return jsonify(errno=RET.NODATA, errmsg='无数据')

    # POST保存指纹
    def post(self):
        try:
            number = request.form.get('number')
            updateDate = int(request.form.get('updateDate'))
            source = request.form.get('source')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate, source]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        try:
            fingerprint = FingerPrint(number=number, updateDate=updateDate, source=source).save()
        except Exception as e:
            current_app.logger.error(e)
            fingerprint = FingerPrint.objects(number=number, source=source).first()
            # 比较更新日期
            if updateDate > fingerprint['updateDate']:
                fingerprint.update(updateDate=updateDate)
                data = {  # 'id': fingerprint.id, # TODO 如何返回ID
                    'number': fingerprint.number,
                    'updateDate': fingerprint.updateDate,
                    'source': fingerprint.source
                }
                return jsonify(errno=RET.UPDATE, errmsg='数据已更新', data=data)
            else:
                return jsonify(errno=RET.DATAEXIST, errmsg='已存在最新数据')
        # 组织返回数据
        data = {  # 'id': fingerprint.id, # TODO 如何返回ID
            'number': fingerprint.number,
            'updateDate': fingerprint.updateDate,
            'source': fingerprint.source}

        return jsonify(errno=RET.OK, errmsg='数据提交成功', data=data)

    # PUT修改指纹
    def put(self):
        try:
            number = request.args.get('number')
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
            number = request.args.get('number')
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

# /lagou 拉勾招聘信息数据视图
class LagouRecruitDataView(views.MethodView):
    def get(self):
        # 控制参数范围
        args = {k:v for k, v in request.args.items()}
        args_keys = [k for k in args]
        validation = [[], ['positionId'], ['page'], ['per_page'], ['page', 'per_page']]
        if args_keys not in validation:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 单个数据
        positionId = request.args.get('positionId')
        if positionId:
            try:
                positionId = int(positionId)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

            from models import LagouData
            position_data = LagouData.objects(positionId=positionId).first()
            if not position_data:
                return jsonify(errno=RET.NODATA, errmsg='数据不存在')
            return jsonify(errno=RET.OK, errmsg='OK', data=position_data.to_dict())

        # 多个数据
        else:
            try:
                page = request.args.get('page', 1)
                per_page = request.args.get('per_page', constants.PER_PAGE_MAX_NUM)
                page = int(page)
                per_page = int(per_page)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

            from models import LagouData
            paginate = LagouData.objects.paginate(page=page, per_page=per_page)
            items = paginate.items
            total_page = paginate.pages
            current_page = paginate.page
            recruit_data = {
                'recruits_list': items,
                'current_page': current_page,
                'total_page': total_page
            }
            return jsonify(errno=RET.OK, errmsg='查询招聘信息列表', data=recruit_data)

    def post(self):
        # 获取参数
        data_dict = {k:v for k,v in request.form.items()}

        # 校验参数
        # 保存数据
        try:
            lagouData = LagouData(**data_dict).save()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据验证错误')
        # 返回结果
        print(lagouData.to_dict())
        return jsonify(lagouData.to_dict())

recruit_bp.add_url_rule('/duplicateChecking', view_func=DuplicateCheckingView.as_view('duplicateCheckingView'))
recruit_bp.add_url_rule('/lagou', view_func=LagouRecruitDataView.as_view('lagouView'))