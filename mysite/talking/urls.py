from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='talking_index_view'),
    url(r'^(?P<slug>[-a-z]+)/$', views.talk, name='talking_talk_view'),
)
                       
