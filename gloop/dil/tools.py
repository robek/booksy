from datetime import datetime
import calendar

def get_week_dates(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year):
    cal = calendar.Calendar(0).monthdayscalendar(year,month)
    week = [ a for a in cal if day in a ][0]
    if week[0] == 0:
        d_month = month - 1
        d_year = year
        if d_month < 1:
            d_year = year - 1
            d_month = d_month + 12

        cal = calendar.Calendar(0).monthdayscalendar(year,d_month)
        sup_week = cal[len(cal)-1]
        for i in range(7):
            if week[i] == 0:
                week[i] = str(sup_week[i]) + "." + str(d_month) + "." + str(d_year)
            else:
                week[i] = str(week[i]) + "." + str(month) + "." + str(year)
    elif week[6] == 0:
        d_month = month + 1
        d_year = year
        if d_month > 12:
            d_year = year + 1
            d_month = d_month - 12
        ins = 1
        for i in range(7):
            if week[i] == 0:
                week[i] = str(ins) + "." + str(d_month) + "." + str(d_year)
                ins = ins + 1
            else:
                week[i] = str(week[i]) + "." + str(month) + "." + str(year)
    else:
        for i in range(7):
            week[i] = str(week[i]) + "." + str(month) + "." + str(year)
    return week

def pack_week(week_days):
    return { 'monday' : '%s' % week_days[0],
             'tuesday' : '%s' % week_days[1],
             'wednesday' : '%s' % week_days[2],
             'thursday' : '%s' % week_days[3],
             'friday' : '%s' % week_days[4],
             'saturday' : '%s' % week_days[5],
             'sunday' : '%s' % week_days[6],
            }


