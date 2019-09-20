import datetime, json, random, itertools
import decimal
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
from django.utils.safestring import SafeString
from .models import Scenic, Recordnums, Recordwarnings, Camera
from dateutil.relativedelta import relativedelta


def test(request):
    # # 添加RecordNums表
    # for i in range(1, 9):  # 8个景区
    #     for j in range(1, 16):  # 5个摄像头位置
    #         for y in range(2, 9):
    #             t = datetime.datetime.now() - relativedelta(months=y)
    #             for k in range(10):  # 10天
    #                 t = t + datetime.timedelta(days=1)
    #                 year = t.year
    #                 month = t.month
    #                 day = t.day
    #                 hour = t.hour
    #                 minute = t.minute
    #                 second = t.second
    #                 createAt = str(t)[:19]
    #                 nums = random.randint(0, 1000)
    #                 sce_obj = Scenic.objects.get(scenicid=i)
    #                 cam_obj = Camera.objects.get(scenicid=i, camid=j)
    #                 Recordnums.objects.create(scenicid=sce_obj, camid=cam_obj, nums=nums, year=year, month=month,
    #                                           day=day,
    #                                           hour=hour,
    #                                           minute=minute, sec=second, createat=createAt)
    # # 添加RecordWarning表
    # for i in range(1, 9):  # 8个景区
    #     t = datetime.datetime.now() - relativedelta(years=0)
    #     for k in range(6 + i):  # 天
    #         t = t + datetime.timedelta(days=1)
    #         createAt = str(t)[:19]
    #         level = random.randint(1, 3)
    #         Recordwarnings.objects.create(scenicid=i, camid=0, level=level, type=1, createat=createAt)
    # # 添加camera表
    # island_names = ['梅峰岛', '黄山尖', '天池岛', '月光岛', '龙山岛', '渔乐岛', '桂花岛', '蜜山岛']
    # lng_list = [118.913233, 119.113483, 119.150892, 119.010011, 118.986830, 118.949720, 119.021276, 119.161023]
    # lat_list = [29.590827, 29.574242, 29.539735, 29.616902, 29.611948, 29.581553, 29.600432, 29.524773]
    # for i in range(0, 8):  # 8个景区
    #     for j in range(0, 16):  # 16个摄像头
    #         lng_rnd = round(random.uniform(0.0001, 0.001), 6)
    #         lat_rnd = round(random.uniform(0.0001, 0.001), 6)
    #         sce_obj = Scenic.objects.get(scenicid=i+1)
    #         Camera.objects.create(camid=j, scenicid=sce_obj, camplace=island_names[i] + '摄像头' + str(j),
    #                               camLng=lng_list[i] + lng_rnd, camlat=lat_list[i] + lat_rnd)
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


def getHeatMapNums(request):
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
        query = "SELECT recordnums.scenicId,recordnums.camId,SUM(nums) AS all_nums,camLng,camLat FROM recordnums,camera WHERE recordnums.camId = camera.camId AND recordnums.scenicId = camera.scenicId AND recordnums.createAt LIKE %s GROUP BY recordnums.scenicId,recordnums.camId"
        cursor.execute(query, [query_time])
        rn_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        res_json[0]['rn_data'] = rn_data
    res_json_seri = json.dumps(res_json)
    return HttpResponse(res_json_seri)


def getHeatMapScenic(request):
    # 封装json
    res_json = [{}]
    # query_time = str(datetime.datetime.now())[0:17] + ‘%’
    query_time = '2019-09-20 15:21%'
    with connection.cursor() as cursor:
        query = "SELECT scenic.scenicId,scenic.scenicName,SUM(nums) as nums,warning1Nums,warning2Nums,warning3Nums,lng,lat FROM scenic,recordnums " \
                "WHERE scenic.scenicId = recordnums.scenicId AND createAt LIKE %s GROUP BY scenicId"
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
