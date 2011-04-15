from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^(?P<slug>[-a-z]+)/$', views.text, name='reading_text_view'),
)
                       
