import json

from flask import current_app, jsonify
from flask import request
from flask import views

from models import FingerPrint
from utils import constants
from utils.response_code import RET
from . import recruit_bp


@recruit_bp.route('/duplicateChecking/<fp>', methods=['GET', 'POST'])
def duplicateChecking(fp):
    result = FingerPrint.objects(fp=fp)
    # GET查询指纹
    if request.method == 'GET':
        if result:
            # print(result.all(), fp)
            return json.dumps({'result': False, 'msg': 'already exist'})
        else:
            return json.dumps({'result': True, 'msg': 'not exist'})
    # POST保存指纹
    if request.method == 'POST':
        if result:
            return json.dumps({'result': False, 'msg': 'already exist'})
        else:
            try:
                fingerprint = FingerPrint(fp=fp).save()
            except Exception as e:
                return json.dumps({'result': False, 'msg': 'MongoDB Error'})
            return json.dumps({'result': True, 'msg': fingerprint.fp})


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


recruit_bp.add_url_rule('/lagou', view_func=LagouRecruitDataView.as_view('lagouView'))