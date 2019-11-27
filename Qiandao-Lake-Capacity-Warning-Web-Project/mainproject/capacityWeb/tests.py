from django.test import TestCase

# Create your tests here.

import datetime
from dateutil.relativedelta import relativedelta

curtime = datetime.datetime.now() + relativedelta(days=1) - relativedelta(years=1)
print(curtime)
