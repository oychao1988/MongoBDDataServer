import json

from datetime import datetime
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
            number = request.args.get('number')
            updateDate = request.args.get('updateDate')
            updateDate = datetime.strptime(updateDate, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerprint = FingerPrint.objects(number=number).first()
        # 能查到number
        if fingerprint:
            # 比较更新日期
            if updateDate > fingerprint['updateDate']:
                return jsonify(errno=RET.UPDATE, errmsg='需要可更新')
            else:
                data = {#'id': fingerprint.id, # TODO 如何返回ID
                        'number': fingerprint.number,
                        'updateDate': fingerprint.updateDate}
                return jsonify(errno=RET.OK, errmsg='成功', data=data)
        return jsonify(errno=RET.NODATA, errmsg='无数据')

    # POST保存指纹
    def post(self):
        try:
            number = request.args.get('number')
            updateDate = request.args.get('updateDate')
            updateDate = datetime.strptime(updateDate, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerprint = FingerPrint.objects(number=number).first()
        # 能查到number
        if fingerprint:
            return jsonify(errno=RET.DATAEXIST, errmsg='数据已存在')
        fingerprint = FingerPrint(number=number, updateDate=updateDate).save()

        # 组织返回数据
        data = {  # 'id': fingerprint.id, # TODO 如何返回ID
            'number': fingerprint.number,
            'updateDate': fingerprint.updateDate}

        return jsonify(errno=RET.OK, errmsg='成功', data=data)

    # PUT修改指纹
    def put(self):
        try:
            number = request.args.get('number')
            updateDate = request.args.get('updateDate')
            updateDate = datetime.strptime(updateDate, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not all([number, updateDate]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不足')
        fingerprint = FingerPrint.objects(number=number).first()
        if not fingerprint:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        # 更新数据
        fingerprint.update(updateDate=updateDate)
        # 组织返回数据
        fingerprint = FingerPrint.objects(number=number).first()
        data = {  # 'id': fingerprint.id, # TODO 如何返回ID
            'number': fingerprint.number,
            'updateDate': fingerprint.updateDate}
        return jsonify(errno=RET.OK, errmsg='成功', data=data)

    # DELETE删除指纹
    def delete(self):
        try:
            number = request.args.get('number')
        except Exception as e:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        if not number:
            jsonify(errno=RET.PARAMERR, errmsg='参数不足')

        fingerPrint = FingerPrint.objects(number=number).first()
        if not fingerPrint:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        fingerPrint.delete()
        return jsonify(errno=RET.OK, errmsg='成功')

# /lagou 拉勾招聘信息数据视图
class LagouRecruitDataView(views.MethodView):
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', constants.PER_PAGE_MAX_NUM)

        try:
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
        return

recruit_bp.add_url_rule('/duplicateChecking', view_func=DuplicateCheckingView.as_view('duplicateCheckingView'))
recruit_bp.add_url_rule('/lagou', view_func=LagouRecruitDataView.as_view('lagouView'))