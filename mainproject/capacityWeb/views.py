import datetime, json, random, itertools
import decimal
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.db import connection
from django.utils.safestring import SafeString
from .models import Scenic, Recordnums, Recordwarnings, Camera
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Min, Max, Sum


def test(request):
    # # 添加RecordNums表
    # for i in range(1, 9):  # 8个景区
    #     for j in range(1, 6):  # 5个摄像头位置
    #         t = datetime.datetime.now() - relativedelta(years=1) + relativedelta(months=2)
    #         for k in range(10):  # 10天
    #             t = t + datetime.timedelta(days=1)
    #             year = t.year
    #             month = t.month
    #             day = t.day
    #             hour = t.hour
    #             minute = t.minute
    #             second = t.second
    #             createAt = str(t)[:19]
    #             nums = random.randint(100, 1000)
    #             sce_obj = Scenic.objects.get(scenicid=i)
    #             cam_obj = Camera.objects.get(scenicid=i, camid=j)
    #             Recordnums.objects.create(scenicid=sce_obj, camid=cam_obj, nums=nums, year=year, month=month,
    #                                       day=day,
    #                                       hour=hour,
    #                                       minute=minute, sec=second, createat=createAt)
    # 添加RecordWarning表
    # for i in range(1, 9):  # 8个景区
    #     t = datetime.datetime.now() - relativedelta(years=0)
    #     for k in range(6 + i):  # 天
    #         t = t + datetime.timedelta(days=1)
    #         createAt = str(t)[:19]
    #         level = random.randint(1, 3)
    #         Recordwarnings.objects.create(scenicid=i, camid=0, level=level, type=1, createat=createAt)
    return render(request, 'test.html')


def getTime(request):
    t = datetime.datetime.now()
    data = {'current_time': str(t)[:17]}
    return HttpResponse(json.dumps(data))


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def get_current_week():
    monday, sunday = datetime.datetime.now(), datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    return monday, sunday


# Create your views here.

def indexV0(request):
    """
    跳转至 indexV0.html
    """
    # 获取时间
    t = datetime.datetime.now()
    return render(request, 'indexV0.html', context={'current_time': t})


def getTouristNums():
    """
    游客人数模块，得到历史游客人数
    :return: context
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    # 本周星期一，星期天
    monday, sunday = get_current_week()
    query_time_monday, query_time_sunday = str(monday)[:19], str(sunday)[:19]
    # 去年同日期
    monday_lastyear, sunday_lastyear = monday - relativedelta(years=1), sunday - relativedelta(years=1)
    query_time_monday_lastyear, query_time_sunday_lastyear = str(monday_lastyear)[:19], str(sunday_lastyear)[:19]
    with connection.cursor() as cursor:
        # 查询本周游客人数
        query = "SELECT SUM(nums) as rn_sum_week FROM recordnums WHERE createAt >= %s AND createAt <= %s"
        cursor.execute(query, [query_time_monday, query_time_sunday])
        rn_sum_week = dictfetchall(cursor)[0]['rn_sum_week']
        # 查询上一年本周游客人数
        query = "SELECT SUM(nums) as rn_sum_week_lastyear FROM recordnums WHERE createAt >= %s AND createAt <= %s"
        cursor.execute(query, [query_time_monday_lastyear, query_time_sunday_lastyear])
        rn_sum_week_lastyear = dictfetchall(cursor)[0]['rn_sum_week_lastyear']
        # 查询本月游客人数
        query = "SELECT SUM(nums) as rn_sum_month FROM recordnums WHERE `year`=%s AND `month` = %s"
        cursor.execute(query, [current_time.year, current_time.month])
        rn_sum_month = dictfetchall(cursor)[0]['rn_sum_month']
        # 查询本月游客人数
        query = "SELECT SUM(nums) as rn_sum_month_lastyear FROM recordnums WHERE `year`=%s AND `month` = %s"
        cursor.execute(query, [current_time.year - 1, current_time.month])
        rn_sum_month_lastyear = dictfetchall(cursor)[0]['rn_sum_month_lastyear']

        context['rn_sum_week'] = rn_sum_week
        context['rn_sum_week_growth'] = rn_sum_week - rn_sum_week_lastyear
        context['rn_sum_week_rate'] = (rn_sum_week - rn_sum_week_lastyear) / rn_sum_week * 100

        context['rn_sum_month'] = rn_sum_month
        # 为了测试！到时改回来
        context['rn_sum_month_growth'] = -(rn_sum_month - rn_sum_month_lastyear)
        context['rn_sum_month_rate'] = -(rn_sum_month - rn_sum_month_lastyear) / rn_sum_month * 100
    return context


def getWarnNums():
    """
    游客人数模块，得到历史游客人数
    :return: context
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    # 本周星期一，星期天
    monday, sunday = get_current_week()
    query_time_monday, query_time_sunday = str(monday)[:19], str(sunday)[:19]
    # 去年同日期
    monday_lastyear, sunday_lastyear = monday - relativedelta(years=1), sunday - relativedelta(years=1)
    query_time_monday_lastyear, query_time_sunday_lastyear = str(monday_lastyear)[:19], str(sunday_lastyear)[:19]
    with connection.cursor() as cursor:
        # 查询本周游客人数
        query = "SELECT COUNT(warningId) as rw_count_week FROM recordwarnings WHERE createAt >= %s AND createAt <= %s"
        cursor.execute(query, [query_time_monday, query_time_sunday])
        rw_count_week = dictfetchall(cursor)[0]['rw_count_week']
        # 查询上一年本周游客人数
        query = "SELECT COUNT(warningId) as rw_count_week_lastyear FROM recordwarnings WHERE createAt >= %s AND createAt <= %s"
        cursor.execute(query, [query_time_monday_lastyear, query_time_sunday_lastyear])
        rw_count_week_lastyear = dictfetchall(cursor)[0]['rw_count_week_lastyear']
        # 查询本月游客人数
        query = "SELECT COUNT(warningId) as rw_count_month FROM recordwarnings WHERE createAt LIKE %s"
        cursor.execute(query, [str(current_time)[:7] + '%'])
        rw_count_month = dictfetchall(cursor)[0]['rw_count_month']
        # 查询本月游客人数
        query = "SELECT COUNT(warningId) as rw_count_month_lastyear FROM recordwarnings WHERE createAt LIKE %s"
        cursor.execute(query, [str(current_time - relativedelta(years=1))[:7] + '%'])
        rw_count_month_lastyear = dictfetchall(cursor)[0]['rw_count_month_lastyear']

        context['rw_count_week'] = rw_count_week
        context['rw_count_week_growth'] = rw_count_week - rw_count_week_lastyear
        context['rw_count_week_rate'] = (rw_count_week - rw_count_week_lastyear) / rw_count_week * 100

        context['rw_count_month'] = rw_count_month
        context['rw_count_month_growth'] = (rw_count_month - rw_count_month_lastyear)
        context['rw_count_month_rate'] = (rw_count_month - rw_count_month_lastyear) / rw_count_month * 100
    return context


def getScenicRank():
    """
    景区人数排行模块
    :return: context:{'scenicrank_data':[{'scenic':'景区1','nums':人数2},...]}
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    with connection.cursor() as cursor:
        # 查询本月游客人数
        query = "SELECT scenicName as scenic,SUM(nums) as nums FROM recordnums,scenic WHERE recordnums.scenicId = scenic.scenicId AND createAt LIKE %s GROUP BY scenic.scenicId ORDER BY nums DESC"
        cursor.execute(query, [str(current_time)[:7] + '%'])
        scenicrank_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        context['scenicrank_data'] = SafeString(scenicrank_data)
    return context


def getWarnRank():
    """
    景区人数排行模块
    :return: context:{'warnrank_data':[{'景区1':次数1,'景区2':次数2},...]}
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    with connection.cursor() as cursor:
        # 查询本月游客人数
        query = "SELECT scenicName AS scenic,COUNT(recordwarnings.scenicId) as times FROM recordwarnings,scenic WHERE recordwarnings.scenicId = scenic.scenicId AND createAt LIKE %s GROUP BY scenic.scenicId ORDER BY times DESC"
        cursor.execute(query, [str(current_time)[:7] + '%'])
        warnrank_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        context['warnrank_data'] = SafeString(warnrank_data)
    return context


def getNumBar():
    """
    景区人数变化模块
    :return: context:{'scenicrank_data':[{'date':'2019-11','nums':人数,'lastyear':人数},...]}
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    with connection.cursor() as cursor:
        # 查询本月游客人数
        query = "SELECT CONCAT(CONCAT(`year`,'-'),`month`) as 'date',SUM(nums) as nums FROM recordnums WHERE `year`=%s GROUP BY `year`,`month` ORDER BY `year` DESC,`month` DESC LIMIT 8"
        cursor.execute(query, [str(current_time.year)])
        numbar_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        query = "SELECT CONCAT(CONCAT(`year`,'-'),`month`) as 'date',SUM(nums) as nums_lastyear FROM recordnums WHERE `year`=%s GROUP BY `year`,`month` ORDER BY `year` DESC,`month` DESC LIMIT 8"
        cursor.execute(query, [str(current_time.year - 1)])
        numbar_data_lastyear = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        for i in range(len(numbar_data)):
            numbar_data[i]['nums_lastyear'] = numbar_data_lastyear[i]['nums_lastyear']
        context['numbar_data'] = SafeString(numbar_data)
    return context


def getCurrentWarn():
    """
    当前预警信息模块
    :return: context:{'scenicrank_data':[{'date':'2019-11','nums':人数,'lastyear':人数},...]}
    """
    context = {}
    # 当前时间
    # current_time = datetime.datetime.now()
    current_time = '2019-09-19 16:10:40'
    with connection.cursor() as cursor:
        # 查询本月游客人数
        query = "SELECT scenicName,camera.camId,`level`,`type` FROM scenic,recordwarnings,camera WHERE recordwarnings.scenicId = scenic.scenicId AND recordwarnings.scenicId = camera.scenicId " \
                "AND recordwarnings.camId = camera.camId AND createAt = %s ORDER BY createAt DESC,level"
        cursor.execute(query, [current_time])
        curwarn_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        context['curwarn'] = curwarn_data
    return context


def getHeatMapPoints(request):
    # 封装json
    res_json = [{}]
    # 景区信息表
    scenic_data = Scenic.objects.all()
    scenic_data_seri = serializers.serialize("json", scenic_data)
    scenic_data = json.loads(scenic_data_seri)
    res_json[0]['scenic_data'] = scenic_data
    # 人数记录表
    # query_time = str(datetime.datetime.now())[0:17] + ‘%’
    query_time = '2019-09-20 15:21%'
    with connection.cursor() as cursor:
        query = "SELECT recordnums.scenicId,recordnums.camId,SUM(nums) AS all_nums,camLgn,camLat FROM recordnums,camera WHERE recordnums.camId = camera.camId AND recordnums.scenicId = camera.scenicId AND recordnums.createAt LIKE %s GROUP BY recordnums.scenicId,recordnums.camId"
        cursor.execute(query, [query_time])
        rn_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        res_json[0]['rn_data'] = rn_data
    res_json_seri = json.dumps(res_json)
    return HttpResponse(res_json_seri)


def index(request):
    """
    跳转至 index.html

    """
    # 参数
    context = {}
    # 游客人数模块
    tourist_context = getTouristNums()
    context.update(tourist_context)
    # 预警次数模块
    warnnums_context = getWarnNums()
    context.update(warnnums_context)
    # 人数排行模块
    scenicrank_context = getScenicRank()
    context.update(scenicrank_context)
    # 预警排行模块
    warnrank_context = getWarnRank()
    context.update(warnrank_context)
    # 景区人数变化模块
    numbar_context = getNumBar()
    context.update(numbar_context)
    # 当前预警信息模块
    curwarn_context = getCurrentWarn()
    context.update(curwarn_context)
    return render(request, 'index.html', context=context)


def meifeng(request):
    """
    :param request:
    :return: 返回梅峰岛景区信息
    """
    # 参数
    context = {}
    # 游客人数模块
    tourist_context = getTouristNums()
    context.update(tourist_context)
    # 预警次数模块
    warnnums_context = getWarnNums()
    context.update(warnnums_context)
    # 人数排行模块
    scenicrank_context = getScenicRank()
    context.update(scenicrank_context)
    # 预警排行模块
    warnrank_context = getWarnRank()
    context.update(warnrank_context)
    # 景区人数变化模块
    numbar_context = getNumBar()
    context.update(numbar_context)
    # 当前预警信息模块
    curwarn_context = getCurrentWarn()
    context.update(curwarn_context)

    return render(request, 'mf_scenic.html', context=context)


def getScenicHeartMapData(request):
    _scenicid = request.GET['_scenicid']  # 后台发送json请求时，附带上岛屿的编号
    _scenicid = int(_scenicid)
    result = Recordnums.objects.values("scenicid", "camid").annotate(latest=Max("id")).filter(scenicid=_scenicid)
    # select scenicid,camid,Max('id') as latest from recordnums where scenucud=1 group by scenicid,camid
    # 因为最新插入的数据id是肯定比之前的大的，所有我们先找到指定岛指定摄像头的数据的最大id

    result_latest = []
    # 存储某一个岛所有摄像头的最新数据
    for i in result:
        # i表示某一个摄像头的数据
        latest_id = i['latest']
        # latest_id 表示i这个摄像头的最新数据的id
        # 字典的访问是i['latest']不是i.latest
        select_latest_nums = Recordnums.objects.filter(id=latest_id).values("scenicid","id", "camid",
                                                                       "nums")
        # 根据最新数据的id来查询Recordnums表，获得人数
        select_latest_nums = select_latest_nums[0]
        # 查询结果是一个list，即使结果只有一个，所以需要[0]
        num = select_latest_nums['nums']
        sceid= select_latest_nums['scenicid']
        cid = select_latest_nums['camid']
        # 获得最新数据的人数num，岛屿id，摄像头id以便查询该摄像头的经纬度
        select_latest_point = Camera.objects.filter(scenicid=sceid, camid=cid).values("camlgn","camlat")
        # 查询Camera表获得经纬度
        result_send = {};
        result_send["count"] = num
        result_send["lng"] = select_latest_point[0]['camlgn']
        result_send["lat"] = select_latest_point[0]['camlat']
        # 按照热力图需要的数据格式存入字典
        result_latest.append(result_send)
        # 将各个摄像头的数据存入result_latest

    return JsonResponse(result_latest, safe=False, json_dumps_params={'ensure_ascii': False})

