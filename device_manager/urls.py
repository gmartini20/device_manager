from django.conf.urls.defaults import patterns, include, url
#from device_manager.views import hello
from django.conf import settings
from device_manager.cadastro.views import list_rooms, edit_rooms, edit_stalls, list_people, edit_people, list_device_category, edit_device_category, list_device, edit_device, edit_trainees

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^hello/$', hello)
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
    url(r'^device/list/$', list_device),
    url(r'^device/edit/$', edit_device),
    url(r'^device/edit/(?P<id>\d+)/$', edit_device),
    url(r'^trainee/edit/$', edit_trainees),
    url(r'^trainee/edit/(?P<id>\d+)/$', edit_trainees),
    
    
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
