from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime, timedelta
from tools import get_week_dates, pack_week

@dajaxice_register
def aPrev(request, date):
    d,m,y = [ int(x) for x in date.split(".") ]
    dd = datetime(day=d, month=m, year=y) - timedelta(days=1)
    week_days = get_week_dates(dd.day, dd.month, dd.year)
    return simplejson.dumps( pack_week(week_days) )

@dajaxice_register
def aNext(request, date):
    d,m,y = [ int(x) for x in date.split(".") ]
    dd = datetime(day=d, month=m, year=y) + timedelta(days=1)
    week_days = get_week_dates(dd.day, dd.month, dd.year)
    return simplejson.dumps( pack_week(week_days) )

