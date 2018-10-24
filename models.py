from apps import mongodb


# 指纹集合
class FingerPrint(mongodb.Document):
    meta = {
        'collection': 'fingerPrint'
    }
    number = mongodb.IntField()
    updateDate = mongodb.IntField()
    source = mongodb.StringField()


# 拉勾招聘信息
class LagouData(mongodb.Document):
    # 指定集合名称
    meta = {'collection': 'lagouRecruit',
            'ordering': ['-createTime'],
            'strict': False,
            }

    # category = mongodb.StringField()  # 工作类别
    # category_url = mongodb.StringField()  # 类别url

    adWord = mongodb.StringField()
    appShow = mongodb.StringField()  # 手机端显示
    approve = mongodb.StringField()  # 同意
    businessZones = mongodb.StringField()  # 商业区域
    city = mongodb.StringField()  # 城市
    companyFullName = mongodb.StringField()  # 公司全称
    companyId = mongodb.StringField()  # 公司ID
    companyLabelList = mongodb.StringField()  # 公司标签列表
    companyLogo = mongodb.StringField()  # 公司logo
    companyShortName = mongodb.StringField()  # 公司简称
    companySize = mongodb.StringField()  # 公司规模
    createTime = mongodb.StringField()  # 发布时间
    deliver = mongodb.StringField()
    district = mongodb.StringField()  # 地区
    education = mongodb.StringField()  # 学历
    explain = mongodb.StringField()
    financeStage = mongodb.StringField()  # 融资阶段
    firstType = mongodb.StringField()  # 工作类型1
    formatCreateTime = mongodb.StringField()
    gradeDescription = mongodb.StringField()
    hitags = mongodb.StringField()
    imState = mongodb.StringField()
    industryField = mongodb.StringField()
    industryLables = mongodb.StringField()
    isSchoolJob = mongodb.StringField()
    jobNature = mongodb.StringField()
    lastLogin = mongodb.StringField()
    linestaion = mongodb.StringField()
    latitude = mongodb.StringField()  # 纬度
    longitude = mongodb.StringField()  # 经度
    pcShow = mongodb.StringField()  # PC端显示
    plus = mongodb.StringField()
    positionAdvantage = mongodb.StringField()  # 职位优势
    positionId = mongodb.StringField()  # 职位编号
    positionLables = mongodb.StringField()  # 职位标签
    positionName = mongodb.StringField()  # 职位名称
    promotionScoreExplain = mongodb.StringField()
    publisherId = mongodb.StringField()
    resumeProcessDay = mongodb.StringField()
    resumeProcessRate = mongodb.StringField()
    salary = mongodb.StringField()  # 薪资
    score = mongodb.StringField()
    secondType = mongodb.StringField()  # 工作类型2
    skillLables = mongodb.StringField()  # 技能标签
    stationname = mongodb.StringField()  # 站点名称
    subwayline = mongodb.StringField()  # 地铁线路
    thirdType = mongodb.StringField()  # 工作类型3
    workYear = mongodb.StringField()  # 工作年限
    description = mongodb.StringField()  # 职位描述
    detailUrl = mongodb.StringField()  # 详情链接

    def to_dict(self):
        data_dict = {
                'businessZones': self.businessZones,  # 商业区域
                'city': self.city,  # 城市
                'companyFullName': self.companyFullName,  # 公司全称
                'companyId': self.companyId,  # 公司ID
                'companyLabelList': self.companyLabelList,  # 公司标签列表
                'companyLogo': self.companyLogo,  # 公司logo
                'companyShortName': self.companyShortName,  # 公司简称
                'companySize': self.companySize,  # 公司规模
                'createTime': self.createTime,  # 发布时间
                'deliver': self.deliver,
                'district': self.district,  # 地区
                'education': self.education,  # 学历
                'explain': self.explain,
                'financeStage': self.financeStage,  # 融资阶段
                'firstType': self.firstType,  # 工作类型1
                'formatCreateTime': self.formatCreateTime,
                'gradeDescription': self.gradeDescription,
                'hitags': self.hitags,
                'imState': self.imState,
                'industryField': self.industryField,
                'industryLables': self.industryLables,
                'isSchoolJob': self.isSchoolJob,
                'jobNature': self.jobNature,
                'lastLogin': self.lastLogin,
                'linestaion': self.linestaion,
                'latitude': self.latitude,  # 纬度
                'longitude': self.longitude,  # 经度
                'pcShow': self.pcShow,  # PC端显示
                'plus': self.plus,
                'positionAdvantage': self.positionAdvantage,  # 职位优势
                'positionId': self.positionId,  # 职位编号
                'positionLables': self.positionLables,  # 职位标签
                'positionName': self.positionName,  # 职位名称
                'promotionScoreExplain': self.promotionScoreExplain,
                'publisherId': self.publisherId,
                'resumeProcessDay': self.resumeProcessDay,
                'resumeProcessRate': self.resumeProcessRate,
                'salary': self.salary,  # 薪资
                'score': self.score,
                'secondType': self.secondType,  # 工作类型2
                'skillLables': self.skillLables,  # 技能标签
                'stationname': self.stationname,  # 站点名称
                'subwayline': self.subwayline,  # 地铁线路
                'thirdType': self.thirdType,  # 工作类型3
                'workYear': self.workYear,  # 工作年限
                'description': self.description,  # 职位描述
                'detailUrl': self.detailUrl,  # 详情链接
        }
        return data_dict

    def __str__(self):
        description = """companyFullName\t:%s,
                         createTime\t:%s,
                         positionName\t:%s,
                         salary\t:%s,
                         businessZones\t:%s
                      """ % (self.companyFullName, self.createTime, self.positionName, self.salary, self.businessZones)
        return description

# 智联招聘信息
class ZhilianItem(mongodb.Document):
    # 指定集合名称
    meta = {'collection': 'zhilianRecruit',
            'ordering': ['-updateDate'],
            'strict': False,
            }

    applied = mongodb.StringField()
    applyType = mongodb.StringField()
    city = mongodb.StringField()
    collected = mongodb.StringField()
    company = mongodb.StringField()
    companyLogo = mongodb.StringField()
    createDate = mongodb.StringField()
    duplicated = mongodb.StringField()
    eduLevel = mongodb.StringField()
    emplType = mongodb.StringField()
    endDate = mongodb.StringField()
    expandCount = mongodb.StringField()
    feedbackRation = mongodb.StringField()
    futureJob = mongodb.StringField()
    geo = mongodb.StringField()
    industry = mongodb.StringField()
    interview = mongodb.StringField()
    isShow = mongodb.StringField()
    jobName = mongodb.StringField()
    jobType = mongodb.StringField()
    number = mongodb.StringField()
    positionLabel = mongodb.StringField()
    positionURL = mongodb.StringField()
    rate = mongodb.StringField()
    recruitCount = mongodb.StringField()
    resumeCount = mongodb.StringField()
    salary = mongodb.StringField()
    saleType = mongodb.StringField()
    score = mongodb.StringField()
    selected = mongodb.StringField()
    showLicence = mongodb.StringField()
    tags = mongodb.StringField()
    timeState = mongodb.StringField()
    updateDate = mongodb.StringField()
    welfare = mongodb.StringField()
    workingExp = mongodb.StringField()