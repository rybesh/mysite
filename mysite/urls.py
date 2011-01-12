from django.conf.urls.defaults import *
from django.contrib import admin
import os.path

media_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
uploads_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))

admin.autodiscover()

urlpatterns = patterns('',
    (r'^favicon.ico$', 'django.views.generic.simple.redirect_to', 
     { 'url': '/media/style/icons/favicon.ico' }),
    (r'^courses/', include('mysite.courses.urls')),
    (r'^admin/', include(admin.site.urls)),

    # The following won't be called in production as Apache will intercept them.
    (r'^media/readings/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': os.path.join(uploads_root, 'readings') }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     { 'document_root': media_root }),
)
