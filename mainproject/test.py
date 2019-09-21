import datetime, random, itertools
from dateutil.relativedelta import relativedelta


def get_current_week():
    monday, sunday = datetime.datetime.now(), datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    return monday, sunday


print(round(random.uniform(0.0001, 0.001), 6))
