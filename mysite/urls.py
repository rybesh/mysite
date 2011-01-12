from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^favicon.ico$', 'django.views.generic.simple.redirect_to', 
     { 'url': '/media/img/favicon.ico' }),
    (r'^courses/', include('mysite.courses.urls')),
    (r'^admin/', include(admin.site.urls)),
)
