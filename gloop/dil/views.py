from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext # for static files/urls
from dil.auth_f import ClientRegistrationForm, CompanyRegistrationForm, LoginForm
from dil.service_f import ServiceForm
from dil.ajax import aPrev, aNext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dil.models import Company, Client, Service
from datetime import datetime
from tools import get_week_dates

def index(request):
    print request.META['REMOTE_ADDR']
    all_comps = Company.objects.all()
    return render_to_response('dil/index.html',
                              { 'all_comps' : all_comps },
                              context_instance=RequestContext(request))

# to refactor: smart models-forms, more fields
def my_register(request):
    client_f = ClientRegistrationForm()
    company_f = CompanyRegistrationForm()
    if request.method == 'POST':
        if "true" in request.POST['is_client']:
            form = ClientRegistrationForm(request.POST)
            kind = 'client'
            client_f = form
        if "true" in request.POST['is_company']:
            form = CompanyRegistrationForm(request.POST)
            kind = 'company'
            company_f = form
        if form.is_valid():
            data = form.cleaned_data
            username = data[kind+'_username']
            password = data[kind+'_password1']
            u = User.objects.create_user(username=username, password=password)
            u.save()
            if 'client' in kind:
                c = Client(base=u)
            if 'company' in kind:
                c = Company(base=u)
            c.save()
            login(request, authenticate(username=username, password=password))
            if 'company' in kind:
                return HttpResponseRedirect('/profile/'+username+'/')
            if 'client' in kind:
                return HttpResponseRedirect('/')

    return render_to_response('dil/register.html', 
                              { 'client_f' : client_f, 'company_f' : company_f }, 
                              context_instance=RequestContext(request) )

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u = authenticate(username=username, password=password)
            if u:
                login(request, u)
                if Company.objects.get_company(u.username):
                    return HttpResponseRedirect('/profile/'+username+'/')
                else:
                    return HttpResponseRedirect('/')

    return render_to_response('dil/login.html',
                              { 'form' : form },
                              context_instance=RequestContext(request))

# Trigger a user logout
def my_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')

def my_profile(request, company_login):
    company = Company.objects.get_company(company_login)
    if not company:
        return HttpResponseRedirect('/')

    date = datetime.now()
    week_dates = get_week_dates(date.day, date.month, date.year)
    schedule = get_schedule(week_dates) # make 30minutes time slots

    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            s_action = form.cleaned_data['service_action']
            s_name = form.cleaned_data['service_name']
            s_prize = form.cleaned_data['service_prize']
            s_duration = form.cleaned_data['service_duration']
            if "new" == s_action:
                s = Service(s_owner=company, s_name=s_name,s_duration=s_duration)
            else:
                original = s_action[5:]
                s = Service.objects.get(s_owner=company, s_name=original)
                s.s_name = s_name
                s.s_duration = s_duration
                print s
            s.save()

    services = Service.objects.filter(s_owner=company)

    return render_to_response('dil/profile.html',
                              { 'company' : company, 'week_days' : week_dates , 'services' : services, 'form' : form },
                               context_instance=RequestContext(request) )

#def add_service(request):
#    lg_user = request.user
#    company = Company.objects.get_company(lg_user.username)
#    if not company:
#        return HttpResponseRedirect('/')
#    if request.method == 'POST':
#        form = ServiceForm(request.POST)
#        if form.is_valid():
#            s_name = form.cleaned_data['name']
#            s_duration = form.cleaned_data['duration']
#            s = Service(owner=company, s_name=s_name, s_duration=s_duration)
#            s.save()
#            return HttpResponseRedirect('profile/' + company + '/')
#    
#    form = ServiceForm()
#    return render_to_response('dil/service.html',
#                              { 'form' : form },
#                              context_instance=RequestContext(request))

def get_schedule(date_string):
    return None
