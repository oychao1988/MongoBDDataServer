from flask import current_app, jsonify
from flask import request
from flask import views

from utils import constants
from utils.response_code import RET
from utils.utils import save
from . import recruit_bp


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
            position_data = self.COLLECTION.find_one({'positionId': positionId})
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

            # TODO 排序检索
            recruits_list = list(self.COLLECTION.find({}).sort("createTime").limit(per_page).skip((page-1)*per_page))
            for data in recruits_list:
                del data['_id']
            count = self.COLLECTION.find({}).count()
            total_page = (count // per_page) + 1
            current_page = page
            recruit_data = {
                'recruits_list': recruits_list,
                'current_page': current_page,
                'total_page': total_page,
            }

            return jsonify(errno=RET.OK, errmsg='查询招聘信息列表', data=recruit_data)

    # 增加职位信息
    def post(self, positionId):
        # 获取参数
        data_dict = {k: str(v) for k, v in request.form.items()}
        # 保存数据
        try:
            data = save(data_dict, COLLECTION=self.COLLECTION, update=True)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据保存错误')
        # 返回结果
        if data:
            return jsonify(errno=RET.OK, errmsg='数据保存成功', data=data)
        else:
            return jsonify(errno=RET.DATAEXIST, errmsg='数据已存在')

    # 更新职位信息
    def put(self, positionId):
        # 参数验证
        try:
            positionId = int(positionId)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        position_data = self.COLLECTION.find_one({'positionId':positionId})
        if not position_data:
            return jsonify(errno=RET.NODATA, errmsg='无数据')

        # 获取参数
        data_dict = {k: str(v) for k, v in request.form.items()}
        # 保存数据
        try:
            self.COLLECTION.update({'positionId':positionId}, data_dict)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据保存错误')
        position_data = self.COLLECTION.find_one({'positionId': positionId})
        return jsonify(errno=RET.OK, errmsg='OK', data=position_data)

    # 删除职位信息
    def delete(self, positionId):
        try:
            positionId = str(positionId)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        # 参数校验
        position_data = self.COLLECTION.find_one({'positionId': positionId})
        if not position_data:
            return jsonify(errno=RET.NODATA, errmsg='无数据')
        self.COLLECTION.delete_one({'positionId': positionId})
        return jsonify(errno=RET.OK, errmsg='OK')

# /lagou 拉勾招聘信息数据视图
class LagouRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').LagouClient

# /zhilian 智联招聘信息数据视图
class ZhilianRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').ZhilianClient

# /liepin 猎聘招聘信息数据视图
class LiepinRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').LiepinClient

# /51job 51job招聘信息数据视图
class Job51RecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').Job51Client

# /zhipin BOSS直聘招聘信息数据视图
class ZhipinRecruitDataView(BaseRecruitDataView):
    COLLECTION = __import__('models').ZhipinClient


# lagou招聘信息试图路由
recruit_bp.add_url_rule('/lagou/', view_func=LagouRecruitDataView.as_view('lagous'), defaults={'positionId': None})
recruit_bp.add_url_rule('/lagou/<int:positionId>', view_func=LagouRecruitDataView.as_view('lagou'),
                        methods=['GET', 'PUT', 'DELETE'])
# /zhilian 智联招聘信息试图路由
recruit_bp.add_url_rule('/zhilian/', view_func=ZhilianRecruitDataView.as_view('zhilians'), defaults={'positionId': None})
recruit_bp.add_url_rule('/zhilian/<int:positionId>', view_func=ZhilianRecruitDataView.as_view('zhilian'),
                        methods=['GET', 'PUT', 'DELETE'])
# /liepin 猎聘招聘信息试图路由
recruit_bp.add_url_rule('/liepin/', view_func=LiepinRecruitDataView.as_view('liepins'), defaults={'positionId': None})
recruit_bp.add_url_rule('/liepin/<int:positionId>', view_func=LiepinRecruitDataView.as_view('liepin'),
                        methods=['GET', 'PUT', 'DELETE'])
# /51job 51job招聘信息试图路由
recruit_bp.add_url_rule('/51job/', view_func=Job51RecruitDataView.as_view('51jobs'), defaults={'positionId': None})
recruit_bp.add_url_rule('/51job/<int:positionId>', view_func=Job51RecruitDataView.as_view('51job'),
                        methods=['GET', 'PUT', 'DELETE'])
# /zhipin BOSS直聘招聘信息试图路由
recruit_bp.add_url_rule('/zhipin/', view_func=ZhipinRecruitDataView.as_view('zhipins'), defaults={'positionId': None})
recruit_bp.add_url_rule('/zhipin/<int:positionId>', view_func=ZhipinRecruitDataView.as_view('zhipin'),
                        methods=['GET', 'PUT', 'DELETE'])