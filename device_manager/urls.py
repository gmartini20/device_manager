from django.conf.urls.defaults import patterns, include, url
#from device_manager.views import hello
from django.conf import settings
from device_manager.cadastro.views import list_rooms, edit_rooms

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^hello/$', hello)
    url(r'^room/list/$', list_rooms),
    url(r'^room/edit/$', edit_rooms),
    url(r'^room/edit/(\d+)/$', edit_rooms),
    
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
