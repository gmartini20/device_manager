from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from device_manager.cadastro.room import list_rooms, edit_rooms
from device_manager.cadastro.stall import edit_stalls
from device_manager.cadastro.trainee import edit_trainees
from device_manager.cadastro.people import list_people, edit_people
from device_manager.cadastro.device_category import list_device_category, edit_device_category, remove_category_device
from device_manager.cadastro.device import list_device, edit_device, remove_device
from device_manager.cadastro.period import edit_period
from device_manager.cadastro.institution import list_institution, edit_institution
from device_manager.cadastro.home import show_home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/$', show_home),
    url(r'^room/list/$', list_rooms),
    url(r'^room/edit/$', edit_rooms),
    url(r'^room/edit/(?P<id>\d+)/$', edit_rooms),
    url(r'^stall/edit/$', edit_stalls),
    url(r'^stall/edit/(?P<id>\d+)/$', edit_stalls),
    url(r'^people/list/$', list_people),
    url(r'^people/edit/$', edit_people),
    url(r'^people/edit/(?P<id>\d+)/$', edit_people),
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
    url(r'^period/edit/$', edit_period),
    url(r'^period/edit/(?P<id>\d+)/$', edit_period),
    url(r'^institution/list/$', list_institution),
    url(r'^institution/edit/$', edit_institution),
    url(r'^institution/edit/(?P<id>\d+)/$', edit_institution),
    
    
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
