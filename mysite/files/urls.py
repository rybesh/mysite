from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^(?P<path>.+(\.pdf|\.zip|\.html|\.doc))$', 
        views.sendfile, name='files_sendfile_view'),
)
