from apps import mongodb


# 指纹集合
class FingerPrint(mongodb.Document):
    meta = {
        'collection': 'fingerPrint'
    }
    fp = mongodb.StringField()


# 拉勾招聘信息
class LagouData(mongodb.Document):
    # 指定集合名称
    meta = {'collection': 'lagouRecruit',
            'ordering': ['-createTime'],
            'strict': False,
            }

    category = mongodb.StringField()  # 工作类别
    category_url = mongodb.StringField()  # 类别url

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

    def __str__(self):
        description = """companyFullName\t:%s,
                         createTime\t:%s,
                         positionName\t:%s,
                         salary\t:%s,
                         businessZones\t:%s
                      """ % (self.companyFullName, self.createTime, self.positionName, self.salary, self.businessZones)
        return description