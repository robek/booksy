from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from datetime import datetime, timedelta
from tools import get_week_dates, pack_week
from dil.models import Company, Client, Service
from dil.service_f import ServiceForm

@dajaxice_register
def change_week_cb(request, date, sign):
    dajax = Dajax()
    d,m,y = [ int(x) for x in date.split(".") ]
    dd = datetime.now()
    if sign == '-':
        dd = datetime(day=d, month=m, year=y) - timedelta(days=1)
    elif sign == '+':
        dd = datetime(day=d, month=m, year=y) + timedelta(days=1)
    else:
        return dajax.json()
    week_days = get_week_dates(dd.day, dd.month, dd.year)    
    for (day, dat) in pack_week(week_days).items():
        dajax.assign('#'+day, 'innerHTML', dat)
    return dajax.json()

@dajaxice_register
def remove_service(request, service):
    dajax = Dajax()
    if not request.user.is_authenticated():
        return dajax.json()
    l_user = request.user.username
    company = Company.objects.get_company(l_user)
    if not company:
        return dajax.json()
    _service = Service.objects.get(s_owner=company, s_name=service)
    if _service:
        _service.delete()
        dajax.redirect("")
    else:
        dajax.alert("could not find service")    
    return dajax.json()

@dajaxice_register
def add_service(request, form):
    print form
    dajax = Dajax()
    if not request.user.is_authenticated():
        return dajax.json()
    company = Company.objects.get_company(request.user.username)
    form = ServiceForm(form)

    if form.is_valid():
        s = Service(s_owner=company, s_name=form.cleaned_data.get('service_name'),
                    s_duration=form.cleaned_data.get('service_duration'),
                    s_price=form.cleaned_data.get('service_price') )
        s.save()
        dajax.redirect("")
    else:
        errors = ""
        for error in form.errors:
            errors = errors + "  " + error
        dajax.alert("Please correct:" + errors)
    return dajax.json()

@dajaxice_register
def edit_service(request, new_title):
    dajax = Dajax()
    dajax.script('cancel_edit();')
    dajax.alert('Save (not)complete using "%s"!' % new_title )
    return dajax.json()

@dajaxice_register
def load_form(request):
    print "dupa"
    dajax = Dajax()
    if not request.user.is_authenticated():
        return dajax.json()
    out = "<legend> Add new </legend>"
    out = out + ServiceForm().as_p()
    out = out + " <p><input type='button' class='btn btn-primary' value='Add!' onclick='send_add();'></p> "

    print out
    dajax.assign('#add_s', 'innerHTML', out)
    return dajax.json()

