from django.conf import settings
from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dil.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^register/$', 'my_register', name='register'),
    url(r'^login/$', 'my_login', name='login'),
    url(r'^profile/(?P<company_login>[\w|\.|\_]+)/$', 'my_profile', name='profile'),
#    url(r'^service/$', 'add_service', name='add_service'),
    url(r'^logout/$', 'my_logout', name='logout'),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    # url(r'^gloop/', include('gloop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
