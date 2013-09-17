from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from device_manager.cadastro.room import list_rooms, edit_rooms, remove_room
from device_manager.cadastro.stall import edit_stalls, remove_stall
from device_manager.cadastro.trainee import edit_trainees, remove_trainee
from device_manager.cadastro.people import list_people, edit_people, remove_people
from device_manager.cadastro.device_category import list_device_category, edit_device_category, remove_category_device
from device_manager.cadastro.device import list_device, edit_device, remove_device
from device_manager.cadastro.period import edit_period, remove_period
from device_manager.cadastro.institution import list_institution, edit_institution, remove_institution
from device_manager.cadastro.home import show_home
from device_manager.cadastro.login import login, logout, redirect_login
from device_manager.cadastro.users import list_user, edit_user, remove_user
from device_manager.cadastro.reports import occupacy_report,period_report,export_occupacy_report,export_period_report
from device_manager.cadastro.profile import list_profile, edit_profile, remove_profile
from device_manager.cadastro.forbidden import forbidden
from device_manager.cadastro.role import list_role, edit_role, remove_role

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^forbidden/$', forbidden),
    url(r'^home/$', show_home),
    url(r'^room/list/$', list_rooms),
    url(r'^room/edit/$', edit_rooms),
    url(r'^room/edit/(?P<id>\d+)/$', edit_rooms),
    url(r'^room/remove/(?P<id>\d+)/$', remove_room),
    url(r'^stall/edit/$', edit_stalls),
    url(r'^stall/edit/(?P<id>\d+)/$', edit_stalls),
    url(r'^stall/remove/(?P<id>\d+)/$', remove_stall),
    url(r'^people/list/$', list_people),
    url(r'^people/edit/$', edit_people),
    url(r'^people/edit/(?P<id>\d+)/$', edit_people),
    url(r'^people/remove/(?P<id>\d+)/$', remove_people),
    url(r'^categorydevice/list/$', list_device_category),
    url(r'^categorydevice/edit/$', edit_device_category),
    url(r'^categorydevice/edit/(?P<id>\d+)/$', edit_device_category),
    url(r'^categorydevice/remove/(?P<id>\d+)/$', remove_category_device),
    url(r'^device/list/$', list_device),
    url(r'^device/edit/$', edit_device),
    url(r'^device/remove/(?P<id>\d+)/$', remove_device),
    url(r'^device/edit/(?P<id>\d+)/$', edit_device),
    url(r'^trainee/edit/$', edit_trainees),
    url(r'^trainee/edit/(?P<id>\d+)/$', edit_trainees),
    url(r'^trainee/remove/(?P<id>\d+)/$', remove_trainee),
    url(r'^period/edit/$', edit_period),
    url(r'^period/edit/(?P<id>\d+)/$', edit_period),
    url(r'^period/remove/(?P<id>\d+)/$', remove_period),
    url(r'^institution/list/$', list_institution),
    url(r'^institution/edit/$', edit_institution),
    url(r'^institution/edit/(?P<id>\d+)/$', edit_institution),
    url(r'^institution/remove/(?P<id>\d+)/$', remove_institution),
    url(r'^reports/occupacy_report/$', occupacy_report),
    url(r'^reports/occupacy_report/(?P<id>.+)/$', occupacy_report),
    url(r'^reports/export_occupacy/$', export_occupacy_report),
    url(r'^reports/export_occupacy/(?P<id>.+)/$', export_occupacy_report),
    url(r'^reports/period_report/$', period_report),
    url(r'^reports/period_report/(?P<id>.+)/$', period_report),
    url(r'^reports/export_period/$', export_period_report),
    url(r'^reports/export_period/(?P<id>.+)/$', export_period_report),
    url(r'^user/list/$', list_user),
    url(r'^user/edit/$', edit_user),
    url(r'^user/edit/(?P<id>\d+)/$', edit_user),
    url(r'^user/remove/(?P<id>\d+)/$', remove_user),
    url(r'^profile/list/$', list_profile),
    url(r'^profile/edit/$', edit_profile),
    url(r'^profile/edit/(?P<id>\d+)/$', edit_profile),
    url(r'^profile/remove/(?P<id>\d+)/$', remove_profile),
    url(r'^role/list/$', list_role),
    url(r'^role/edit/$', edit_role),
    url(r'^role/remove/(?P<id>\d+)/$', remove_role),
    url(r'^role/edit/(?P<id>\d+)/$', edit_role),
    
    
    # Examples:
    # url(r'^$', 'device_manager.views.home', name='home'),
    # url(r'^device_manager/', include('device_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
