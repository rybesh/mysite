from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^myposts/$', views.myposts, name='blog_myposts'),
)
