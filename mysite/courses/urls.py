from django.conf.urls.defaults import *
import views

course_patterns = patterns('',
    url(r'^$', 
        views.info, name='course_info_view'),
    url(r'^schedule/$', 
        views.schedule, name='course_schedule_view'),
    url(r'^guidelines/$', 
        views.guidelines, name='course_guidelines_view'),
    url(r'^assignments/$', 
        views.assignments, name='course_assignments_view'),
)
urlpatterns = patterns('',
    url(r'^(?P<slug>[a-z]+-\d+)/blog/$', 
        views.blog, name='course_blog_view'),
    url(r'^(?P<slug>[a-z]+-\d+)/blog/new/post/$', 
        views.edit_post, name='course_blog_new_post_view'),
    url(r'^(?P<slug>[a-z]+-\d+)/blog/(?P<post_slug>[-a-z0-9]+)/$', 
        views.blog, name='course_blog_post_view'),
    url(r'^(?P<slug>[a-z]+-\d+)/blog/(?P<post_slug>[-a-z0-9]+)/edit/$', 
        views.edit_post, name='course_blog_edit_post_view'),
    (r'^(?P<slug>[a-z]+-\d+)/(?P<year>\d{4})/(?P<semester>sp|su|fa)/', 
        include(course_patterns)),
    url(r'^discuss/(?P<discussion_id>\d+)',
        views.discussion, name='course_discussion_view'),
)

