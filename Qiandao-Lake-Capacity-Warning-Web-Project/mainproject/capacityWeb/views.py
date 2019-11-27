import time, datetime, json, random, itertools
import decimal
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import connection
from django.utils.safestring import SafeString
from .models import Scenic, Recordnums, Recordwarnings, Camera
from dateutil.relativedelta import relativedelta
from django.db.models import Max, Sum


def test(request):
    result = Recordnums.objects.filter(minute__modEqual=5).values('scenicid', 'month')
    return render(request, 'test.html')


def addData(request):
    # 添加Recordwarnings表
    for i in range(20):
        curtime = datetime.datetime.now() + relativedelta(days=i) - relativedelta(years=1)
        for j in range(1, 9):
            level = random.randint(1, 3)
            Recordwarnings.objects.create(scenicid=j, camid=0, level=level, type=1, createat=str(curtime)[:19])
    # 添加Recordnums表
    for i in range(20):
        curtime = datetime.datetime.now() + relativedelta(days=i) - relativedelta(years=1)
        year = curtime.year
        month = curtime.month
        day = curtime.day
        hour = curtime.hour
        minute = curtime.minute
        sec = curtime.second
        for j in range(1, 9):
            for k in range(1, 16):
                nums = random.randint(1, 1000)
                sce_obj = Scenic(scenicid=j)
                cam_obj = Camera(scenicid=sce_obj, camid=k)
                Recordnums.objects.create(scenicid=sce_obj, camid=cam_obj, nums=nums, year=year, month=month, day=day,
                                          hour=hour,
                                          minute=minute, sec=sec, createat=str(curtime)[:19])
    return render(request, 'addData.html')


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
    # 返回当前的星期一前一天和星期天后一天
    return monday - relativedelta(days=1), sunday + relativedelta(days=1)


def get_time_dic():
    curtime = datetime.datetime.now()
    monday, sunday = datetime.datetime.now(), datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    time_dic = {'monday': monday - relativedelta(days=1), 'sunday': sunday + relativedelta(days=1),
                'last_monday': monday - relativedelta(days=8), 'last_sunday': monday}
    lastmonth_time = curtime - relativedelta(months=1)
    time_dic['lastmonth_year'] = lastmonth_time.year
    time_dic['lastmonth_month'] = lastmonth_time.month
    time_dic['lastmonth'] = lastmonth_time
    # 返回timedate字典
    return time_dic


def getIntervalTouristNums(start, end, scenicid):
    """
    :param start:
    :param end:
    :return: 获得start-end时间端内某岛的人数
    """
    nums_this_Interval = Recordnums.objects.filter(scenicid=scenicid, year__range=[start.year, end.year],
                                                   month__range=[start.month, end.month],
                                                   day__range=[start.day, end.day],
                                                   ).values("nums")
    sum_ = 0
    for r in nums_this_Interval:
        sum_ += r['nums']
    return sum_


def getIntervalWarnNums(start, end, scenicid):
    """

    :param start:
    :param end:
    :param scenicid:
    :return: 获得某岛的一段时间内的预警次数
    """
    start_str = str(start)[:10]
    end = end + relativedelta(days=1)  # 因为是半闭合区间
    end_str = str(end)[:10]

    sum_ = 0
    result = Recordwarnings.objects.filter(scenicid=scenicid, createat__gt=start_str, createat__lt=end_str)
    for r in result:
        sum_ += 1

    return sum_


def getYouNeedInterval():
    """

    :return:获得本周起始时间，上一周起始时间，去年的本周起始时间，
            本月份起始时间，上一个月起始时间，去年本月起始时间
    """
    current_time = datetime.datetime.now()
    month_today = current_time
    month_start = current_time - relativedelta(days=current_time.day - 1)

    month_start_lastyear, month_today_lastyear = month_start - relativedelta(years=1), month_today - relativedelta(
        years=1)
    month_start_lastmonth, month_today_lastmonth = month_start - relativedelta(months=1), month_today - relativedelta(
        months=1)
    # 获得本月的起始时间，去年的本月起始时间，上个月的起始时间

    monday, sunday = get_current_week()
    sunday = current_time
    monday_lastyear, sunday_lastyear = monday - relativedelta(years=1), sunday - relativedelta(years=1)
    monday_lastweek, sunday_lastweek = monday - relativedelta(days=7), sunday - relativedelta(days=7)

    # 获得本周的起始时间，去年的本周起始时间，上周起始时间

    return monday, sunday, monday_lastweek, sunday_lastweek, monday_lastyear, sunday_lastyear, \
           month_start, month_today, month_start_lastmonth, month_today_lastmonth, month_start_lastyear, \
           month_today_lastyear


def getYearOverYearRate(nowDate, prevDate):
    """

    :param nowDate:
    :param prevDate:
    :return:返回同比增长率
    """
    return (nowDate - prevDate) / (nowDate + 1) * 100


def getMonthOverMonthRate(nowDate, prevDate):
    """

    :param nowDate:
    :param prevDate:
    :return: 返回环比增长率
    """
    return (nowDate - prevDate) / (prevDate + 1) * 100


def getScenicTouristNums(scenicid):
    """

    :param scenicid:
    :return: 得到某岛旅客人数
    """
    contexts = {}

    monday, sunday, monday_lastweek, sunday_lastweek, monday_lastyear, sunday_lastyear, \
    month_start, month_today, month_start_lastmonth, month_today_lastmonth, month_start_lastyear, \
    month_today_lastyear = getYouNeedInterval()

    # 获得本周的起始时间，去年的本周起始时间，上周起始时间
    # 本月份起始时间，上一个月起始时间，去年本月起始时间
    num_this_month = getIntervalTouristNums(month_start, month_today, scenicid)
    num_this_month_lastyear = getIntervalTouristNums(month_start_lastyear, month_today_lastyear, scenicid)
    num_this_month_lastmonth = getIntervalTouristNums(month_start_lastmonth, month_today_lastmonth, scenicid)
    # 通过getIntervalTouristNums获得本月份，去年本月份，上个月的游客人数

    month_yearOveryear_rate = getYearOverYearRate(num_this_month, num_this_month_lastyear)
    month_monthOvermonth_rate = getMonthOverMonthRate(num_this_month, num_this_month_lastmonth)
    contexts['month_yearOveryear_rate'] = month_yearOveryear_rate
    contexts['month_monthOvermonth_rate'] = month_monthOvermonth_rate
    contexts['num_this_month'] = num_this_month
    # 计算出月同比和环比增长率和环比率比保存到contexts中

    num_this_week = getIntervalTouristNums(monday, sunday, scenicid)
    num_this_week_lastyear = getIntervalTouristNums(monday_lastyear, sunday_lastyear, scenicid)
    num_this_week_lastweek = getIntervalTouristNums(monday_lastweek, sunday_lastweek, scenicid)
    # 通过getIntervalTouristNums获得本周，去年本周，上周的游客人数

    week_yearOveryear_rate = getYearOverYearRate(num_this_week, num_this_week_lastyear)
    week_weekOverweek_rate = getMonthOverMonthRate(num_this_week, num_this_week_lastweek)
    contexts['week_yearOveryear_rate'] = week_yearOveryear_rate
    contexts['week_weekOverweek_rate'] = week_weekOverweek_rate
    contexts['num_this_week'] = num_this_week
    # 计算出周的同比增长率和环比增长率并保存到contexts字典中

    return contexts


def getTouristNums():
    """
    游客人数模块，得到历史游客人数
    :return: context
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    # 所需时间
    time_dic = get_time_dic()
    # query_time_monday, query_time_sunday = str(time_dic['monday'])[:10], str(time_dic['sunday'])[:10]
    # query_time_monday_lastweek, query_time_sunday_lastweek = str(time_dic['last_monday'])[:10], str(time_dic['last_sunday'])[:10]
    query_time_monday, query_time_sunday = '2019-09-22', '2019-09-30'
    query_time_monday_lastweek, query_time_sunday_lastweek = '2019-09-15', '2019-09-23'
    # 去年同日期
    # monday_lastyear, sunday_lastyear = time_dic['monday'] - relativedelta(years=1), time_dic['sunday'] - relativedelta(years=1)
    # query_time_monday_lastyear, query_time_sunday_lastyear = str(monday_lastyear)[:10], str(sunday_lastyear)[:10]
    query_time_monday_lastyear, query_time_sunday_lastyear = '2018-09-22', '2018-09-30'
    with connection.cursor() as cursor:
        # 查询本周游客人数
        query = "SELECT SUM(nums) as rn_sum_week FROM recordnums WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday, query_time_sunday])
        rn_sum_week = dictfetchall(cursor)[0]['rn_sum_week']
        # 查询上一周游客人数
        query = "SELECT SUM(nums) as rn_sum_week_lastweek FROM recordnums WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday_lastweek, query_time_sunday_lastweek])
        rn_sum_week_lastweek = dictfetchall(cursor)[0]['rn_sum_week_lastweek']
        # 查询上一年本周游客人数
        query = "SELECT SUM(nums) as rn_sum_week_lastyear FROM recordnums WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday_lastyear, query_time_sunday_lastyear])
        rn_sum_week_lastyear = dictfetchall(cursor)[0]['rn_sum_week_lastyear']
        # 查询本月游客人数
        query = "SELECT SUM(nums) as rn_sum_month FROM recordnums WHERE `year`=%s AND `month` = %s"
        # cursor.execute(query, [current_time.year, current_time.month])
        cursor.execute(query, [2019, 9])
        rn_sum_month = dictfetchall(cursor)[0]['rn_sum_month']
        # 查询上一月游客人数
        query = "SELECT SUM(nums) as rn_sum_month_lastmonth FROM recordnums WHERE `year`=%s AND `month` = %s"
        # cursor.execute(query, [time_dic['lastmonth_year'], time_dic['lastmonth_month']])
        cursor.execute(query, [2019, 8])
        rn_sum_month_lastmonth = dictfetchall(cursor)[0]['rn_sum_month_lastmonth']
        # 查询上一年本月游客人数
        query = "SELECT SUM(nums) as rn_sum_month_lastyear FROM recordnums WHERE `year`=%s AND `month` = %s"
        # cursor.execute(query, [current_time.year - 1, current_time.month])
        cursor.execute(query, [2018, 9])
        rn_sum_month_lastyear = dictfetchall(cursor)[0]['rn_sum_month_lastyear']

        context['rn_sum_week'] = rn_sum_week
        context['rn_sum_week_wow'] = (rn_sum_week - rn_sum_week_lastweek) / (rn_sum_week_lastweek + 1) * 100
        context['rn_sum_week_yoy'] = (rn_sum_week - rn_sum_week_lastyear) / (rn_sum_week_lastyear + 1) * 100
        context['rn_sum_month'] = rn_sum_month
        context['rn_sum_month_mom'] = (rn_sum_month - rn_sum_month_lastmonth) / (rn_sum_month_lastmonth + 1) * 100
        context['rn_sum_month_yoy'] = (rn_sum_month - rn_sum_month_lastyear) / (rn_sum_month_lastyear + 1) * 100
    return context


def getScenicWarntNums(scenicid):
    contexts = {}

    monday, sunday, monday_lastweek, sunday_lastweek, monday_lastyear, sunday_lastyear, \
    month_start, month_today, month_start_lastmonth, month_today_lastmonth, month_start_lastyear, \
    month_today_lastyear = getYouNeedInterval()
    # 获得本周的起始时间，去年的本周起始时间，上周起始时间
    # 本月份起始时间，上一个月起始时间，去年本月起始时间

    num_this_month = getIntervalWarnNums(month_start, month_today, scenicid)
    num_this_month_lastyear = getIntervalWarnNums(month_start_lastyear, month_today_lastyear, scenicid)
    num_this_month_lastmonth = getIntervalWarnNums(month_start_lastmonth, month_today_lastmonth, scenicid)
    # 通过getIntervalWarnNums获得本月份，去年本月份，上个月的预警次数

    month_yearOveryear_rate_warn = getYearOverYearRate(num_this_month, num_this_month_lastyear)
    month_monthOvermonth_rate_warn = getMonthOverMonthRate(num_this_month, num_this_month_lastmonth)
    contexts['month_yearOveryear_rate_warn'] = month_yearOveryear_rate_warn
    contexts['month_monthOvermonth_rate_warn'] = month_monthOvermonth_rate_warn
    contexts['num_this_month_warn'] = num_this_month
    # 计算出月同比和环比增长率和环比率比保存到contexts中

    num_this_week = getIntervalWarnNums(monday, sunday, scenicid)
    num_this_week_lastyear = getIntervalWarnNums(monday_lastyear, sunday_lastyear, scenicid)
    num_this_week_lastweek = getIntervalWarnNums(monday_lastweek, sunday_lastweek, scenicid)
    # 通过getIntervalWarnNums获得本周，去年本周，上周的游客人数

    week_yearOveryear_rate_warn = getYearOverYearRate(num_this_week, num_this_week_lastyear)
    week_weekOverweek_rate_warn = getMonthOverMonthRate(num_this_week, num_this_week_lastweek)
    contexts['week_yearOveryear_rate_warn'] = week_yearOveryear_rate_warn
    contexts['week_weekOverweek_rate_warn'] = week_weekOverweek_rate_warn
    contexts['num_this_week_warn'] = num_this_week
    # 计算出周的同比增长率和环比增长率并保存到contexts字典中

    return contexts


def getWarnNums():
    """
    预警次数模块，得到历史预警次数
    :return: context
    """
    context = {}
    # 当前时间
    current_time = datetime.datetime.now()
    # 所需时间
    time_dic = get_time_dic()
    # query_time_monday, query_time_sunday = str(time_dic['monday'])[:10], str(time_dic['sunday'])[:10]
    # query_time_monday_lastweek, query_time_sunday_lastweek = str(time_dic['last_monday'])[:10], str(time_dic['last_sunday'])[:10]
    query_time_monday, query_time_sunday = '2019-09-22', '2019-09-30'
    query_time_monday_lastweek, query_time_sunday_lastweek = '2019-09-15', '2019-09-23'
    # 去年同日期
    # monday_lastyear, sunday_lastyear = time_dic['monday'] - relativedelta(years=1), time_dic['sunday'] - relativedelta(years=1)
    # query_time_monday_lastyear, query_time_sunday_lastyear = str(monday_lastyear)[:10], str(sunday_lastyear)[:10]
    query_time_monday_lastyear, query_time_sunday_lastyear = '2018-09-22', '2018-09-30'
    with connection.cursor() as cursor:
        # 查询本周游客人数
        query = "SELECT COUNT(warningId) as rw_count_week FROM recordwarnings WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday, query_time_sunday])
        rw_count_week = dictfetchall(cursor)[0]['rw_count_week']
        # 查询上一周游客人数
        query = "SELECT COUNT(warningId) as rw_count_week_lastweek FROM recordwarnings WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday_lastweek, query_time_sunday_lastweek])
        rw_count_week_lastweek = dictfetchall(cursor)[0]['rw_count_week_lastweek']
        # 查询上一年本周游客人数
        query = "SELECT COUNT(warningId) as rw_count_week_lastyear FROM recordwarnings WHERE createAt > %s AND createAt < %s"
        cursor.execute(query, [query_time_monday_lastyear, query_time_sunday_lastyear])
        rw_count_week_lastyear = dictfetchall(cursor)[0]['rw_count_week_lastyear']
        # 查询本月游客人数
        query = "SELECT COUNT(warningId) as rw_count_month FROM recordwarnings WHERE createAt LIKE %s"
        cursor.execute(query, [str(current_time)[:7] + '%'])
        rw_count_month = dictfetchall(cursor)[0]['rw_count_month']
        # 查询上一月游客人数
        query = "SELECT COUNT(warningId) as rw_count_month_lastmonth FROM recordwarnings WHERE createAt LIKE %s"
        cursor.execute(query, [str(time_dic['lastmonth'])[:7] + '%'])
        rw_count_month_lastmonth = dictfetchall(cursor)[0]['rw_count_month_lastmonth']
        # 查询本月游客人数
        query = "SELECT COUNT(warningId) as rw_count_month_lastyear FROM recordwarnings WHERE createAt LIKE %s"
        cursor.execute(query, [str(current_time - relativedelta(years=1))[:7] + '%'])
        rw_count_month_lastyear = dictfetchall(cursor)[0]['rw_count_month_lastyear']

        context['rw_count_week'] = rw_count_week
        context['rw_count_week_wow'] = (rw_count_week - rw_count_week_lastweek) / (rw_count_week_lastweek + 1) * 100
        context['rw_count_week_yoy'] = (rw_count_week - rw_count_week_lastyear) / (rw_count_week_lastyear + 1) * 100
        context['rw_count_month'] = rw_count_month
        context['rw_count_month_mom'] = (rw_count_month - rw_count_month_lastmonth) / (
                rw_count_month_lastmonth + 1) * 100
        context['rw_count_month_yoy'] = (rw_count_month - rw_count_month_lastyear) / (rw_count_month_lastyear + 1) * 100
    return context


def getScenicPlaceRank_week(scenicid_):
    """

    :param scenicid:
    :return: 获得某一个岛屿本周人数排行
    """
    current_time = datetime.datetime.now()
    monday, sunday = get_current_week()
    week_end = current_time + relativedelta(days=1)
    week_end_str = str(week_end)[:10]
    week_start_str = str(monday)[:10]
    # 获得本月起始时间与当前时间的字符串形式

    result = Recordnums.objects.filter(scenicid=scenicid_, createat__gt=week_start_str,
                                       createat__lt=week_end_str).values('camid').annotate(
        sun_num=Sum("nums")).order_by('sun_num')
    # 获得代号为scenicid_岛的各个摄像头的本月人流量

    tourist_num = []
    places = []
    for r in result:
        tourist_num.append(r['sun_num'])
        place = Camera.objects.filter(scenicid=scenicid_, camid=r['camid']).values('camplace')[0]['camplace']
        places.append(place)
    # 因为利用直方图来显示的时候需要categories和date，所以将其分别放入places和tourist_num
    scenicplacerankweek_context = {'place_week_rank': places, 'nums_week_rank': tourist_num}
    return scenicplacerankweek_context


def getScenicPlaceRank(scenicid_):
    """
    得到某一个岛的本月从月初到现在的游客人数排行榜
    :param scenicid_:
    :return: {'data':[data]},{'places':[placename]}
    """
    current_time = datetime.datetime.now()
    month_start = current_time - relativedelta(days=current_time.day - 1)
    month_end = current_time + relativedelta(days=1)
    month_end_str = str(month_end)[:10]
    month_start_str = str(month_start)[:10]
    # 获得本月起始时间与当前时间的字符串形式

    result = Recordnums.objects.filter(scenicid=scenicid_, createat__gt=month_start_str,
                                       createat__lt=month_end_str).values('camid').annotate(
        sun_num=Sum("nums")).order_by('sun_num')
    # 获得代号为scenicid_岛的各个摄像头的本月人流量

    tourist_num = []
    places = []
    for r in result:
        tourist_num.append(r['sun_num'])
        place = Camera.objects.filter(scenicid=scenicid_, camid=r['camid']).values('camplace')[0]['camplace']
        places.append(place)
    # 因为利用直方图来显示的时候需要categories和date，所以将其分别放入places和tourist_num
    scenicplacerank_context = {'place_month_rank': places, 'nums_month_rank': tourist_num}
    return scenicplacerank_context


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
    预警次数排行模块
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


def getHeatMapCamera(request):
    # 封装json
    res_json = [{}]
    with connection.cursor() as cursor:
        query = "SELECT * FROM camera WHERE camId!=0"
        cursor.execute(query)
        camera_data = json.loads(json.dumps(dictfetchall(cursor), cls=DecimalEncoder))
        res_json[0]['camera_data'] = camera_data
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
    context = getScenicContext(1)
    return render(request, 'mf_scenic.html', context=context)


def huangshanjian(request):
    """

    :param request:
    :return: 返回黄山尖景区信息
    """
    context = getScenicContext(2)
    return render(request, 'hs_scenic.html', context=context)


def tianchi(request):
    """

    :param request:
    :return: 返回天池岛景区信息
    """
    context = getScenicContext(3)
    return render(request, 'tc_scenic.html', context=context)


def yueguang(request):
    """

    :param request:
    :return: 返回月光岛景区信息
    """
    context = getScenicContext(4)
    return render(request, 'yg_scenic.html', context=context)


def longshan(request):
    """

    :param request:
    :return: 返回龙山岛景区信息
    """
    context = getScenicContext(5)
    return render(request, 'longshan_scenic.html', context=context)


def yule(request):
    """

    :param request:
    :return: 返回渔乐岛景区信息
    """
    context = getScenicContext(6)
    return render(request, 'yl_scenic.html', context=context)


def guihua(request):
    """

    :param request:
    :return: 返回桂花岛景区信息
    """

    context = getScenicContext(7)
    return render(request, 'gh_scenic.html', context=context)


def mishan(request):
    """

    :param request:
    :return: 返回蜜山岛信息
    """
    context = getScenicContext(8)
    return render(request, 'ms_scenic.html', context=context)


def getScenicContext(scenicid_):
    context = {}

    # 岛屿参数
    info_context = getScenicInfo(scenicid_)
    context.update(info_context)
    # 游客人数模块
    tourist_context = getScenicTouristNums(scenicid_)
    context.update(tourist_context)
    # 预警次数模块
    warnnums_context = getScenicWarntNums(scenicid_)
    context.update(warnnums_context)
    # 本月人数排行模块
    scenicplacerank_context = getScenicPlaceRank(scenicid_)
    context.update(scenicplacerank_context)
    # 本周人数排行模块
    scenicplacerankweek_context = getScenicPlaceRank_week(scenicid_)
    context.update(scenicplacerankweek_context)
    # 景区人数变化模块
    numbar_context = todayTouristNumChangeStart(scenicid_)
    context.update(numbar_context)
    # 当前预警信息模块
    curwarn_context = getCurrentWarn()
    context.update(curwarn_context)
    # 游客人数分布模块
    distribute_context = getTouristDistribute(scenicid_)
    context.update(distribute_context)

    return context


def getScenicHeartMapData(request):
    """

    :param request:
    :return:根据request中的scenicid返回对应岛屿的热度图
    """
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
        select_latest_nums = Recordnums.objects.filter(id=latest_id).values("scenicid", "id", "camid",
                                                                            "nums")
        # 根据最新数据的id来查询Recordnums表，获得人数
        select_latest_nums = select_latest_nums[0]
        # 查询结果是一个list，即使结果只有一个，所以需要[0]
        num = select_latest_nums['nums']
        sceid = select_latest_nums['scenicid']
        cid = select_latest_nums['camid']
        # 获得最新数据的人数num，岛屿id，摄像头id以便查询该摄像头的经纬度
        select_latest_point = Camera.objects.filter(scenicid=sceid, camid=cid).values("camlng", "camlat")
        # 查询Camera表获得经纬度
        result_send = {}
        result_send["count"] = num
        result_send["lng"] = select_latest_point[0]['camlng']
        result_send["lat"] = select_latest_point[0]['camlat']
        # 按照热力图需要的数据格式存入字典
        result_latest.append(result_send)
        # 将各个摄像头的数据存入result_latest

    return JsonResponse(result_latest, safe=False, json_dumps_params={'ensure_ascii': False})


def todayTouristNumChangeStart(scenicid):
    start_data = getTodayIntervalTouristNums(scenicid)
    start_data_week = getThisWeekTouristNums(scenicid)
    start_data_month = getThisMonthTouristNums(scenicid)
    context = {'start_data': start_data, 'start_data_week': start_data_week, 'start_data_month': start_data_month}
    return context


def getThisWeekTouristNums(scencicid=1):
    """

    :param scencicid:
    :return: 返回本周内人数
    """
    monday, sunday = get_current_week()
    monday = monday + relativedelta(days=1)
    today = datetime.datetime.now()

    result = Recordnums.objects.filter(scenicid=scencicid, day__gte=monday.day, day__lte=today.day \
                                       , year__gte=monday.year, year__lte=today.year, \
                                       month__gte=monday.month, month__lte=today.month).values('year', 'month',
                                                                                               'day').annotate(
        weeknums=Sum('nums')).order_by('-year', '-month', '-day')
    result_send = []
    for i, r in enumerate(result):
        nums = r['weeknums']
        timeArray = time.strptime(str(r['year']) + '-' + str(r['month']) + '-' + str(r['day']), '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        result_item = [timeStamp, nums]
        result_send.append(result_item)
    return result_send


def getThisMonthTouristNums(scencicid=1):
    """

    :param scencicid:
    :return: 返回本月份内人数
    """

    today = datetime.datetime.now()
    start = today - relativedelta(days=today.day - 1)
    result = Recordnums.objects.filter(scenicid=scencicid, day__gte=start.day, day__lte=today.day \
                                       , year__gte=start.year, year__lte=today.year, month__gte=start.month,
                                       month__lte=today.month).values('year', 'month', 'day').annotate(
        weeknums=Sum('nums')).order_by('-year', '-month', '-day')
    result_send = []
    for r in result:
        nums = r['weeknums']
        timeArray = time.strptime(str(r['year']) + '-' + str(r['month']) + '-' + str(r['day']), '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        result_item = [timeStamp, nums]
        result_send.append(result_item)
    return result_send


def getTodayIntervalTouristNums(scenicid_=1):
    """

    :return: 返回当前时间到1小时前的间隔内的数据
    """
    today_now = datetime.datetime.now() - relativedelta(month=9)  # 改
    today_now = today_now - relativedelta(days=today_now.day - 28)
    # 在展示demo的时候我们只展示9-28的数据。部署的时候再来具体更改
    today_start = today_now - relativedelta(minutes=60)
    today_start_str = str(today_start)[:19]
    today_now_str = str(today_now)[:19]

    result = Recordnums.objects.filter(scenicid=scenicid_, createat__gt=today_start_str,
                                       createat__lt=today_now_str, sec=0).values(
        'createat').annotate(all_nums=Sum('nums')).order_by('createat')
    result_send = []
    for r in result:
        timeArray = time.strptime(r['createat'], '%Y-%m-%d %H:%M:%S')
        timeStamp = int(time.mktime(timeArray)) * 1000
        nums = r['all_nums']
        result_item = [timeStamp, nums]
        result_send.append(result_item)
    return result_send


def updatetodayTouristNums(request):
    scenicid = request.GET['scenicid']
    scenicid = int(scenicid)
    result_send = getTodayIntervalTouristNums(scenicid)
    return JsonResponse(result_send, safe=False)


def getTouristDistribute(scencid_):
    '''

    :param scencid_:
    :return: 得到某岛今年与去年的各月份人数分布
    '''
    current_time = datetime.datetime.now()
    last_time = current_time - relativedelta(years=1)
    # 得到去年今日和今年今日时间

    this_year = current_time.year
    last_year = last_time.year

    query_this_year = Recordnums.objects.filter(scenicid=scencid_, year=this_year).values('month'). \
        annotate(sum_num=Sum('nums'))
    query_last_year = Recordnums.objects.filter(scenicid=scencid_, year=last_year).values('month'). \
        annotate(sum_num=Sum('nums'))

    result_this_year = []
    result_last_year = []
    for r in query_last_year:
        one_month = {'value': r['sum_num'], 'name': r['month']}
        result_last_year.append(one_month)
    for r in query_this_year:
        one_month = {'value': r['sum_num'], 'name': r['month']}
        result_this_year.append(one_month)
    result_send = {'distribute_lastYear': result_last_year, 'distribute_thisYear': result_this_year}
    return result_send


def getScenicInfo(scencid_):
    result = Scenic.objects.filter(scenicid=scencid_).values()
    result_send = {}
    result_send['NAME'] = result[0]['scenicname']
    result_send['scenic_lng'] = result[0]['lng']
    result_send['scenic_lat'] = result[0]['lat']
    result_send['scenic_id'] = result[0]['scenicid']
    return result_send


# 最新预警信息
def latestwarn(request):
    return render(request, 'latestwarn.html')
