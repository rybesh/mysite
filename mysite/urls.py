from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import redirect_to, direct_to_template

admin.autodiscover()

@login_required
def loggedin(request):
    if request.user.is_staff:
        return redirect('/admin/')
    for course in request.user.courses.all()[:1]:
        return redirect(course)
    return redirect('/')

urlpatterns = patterns('',
    url(r'^deploy/$', 'mysite.shared.views.deploy', name='shared_deploy_view'),

    (r'^$', direct_to_template, { 'template': 'bio.html' }),

    (r'^dissertation/$', direct_to_template, 
     { 'template': 'dissertation.html' }),

    (r'^favicon.ico$', redirect_to, { 'url': '/media/img/favicon.ico' }),

    (r'^short/', include('shorturls.urls')),

    (r'^reading/', include('mysite.reading.urls')),

    (r'^courses/', include('mysite.courses.urls')),

    url(r'^comments/post/$', 'mysite.comments.views.post_comment', 
        name='comments_post_comment_view'),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^loggedin/$', loggedin),

    (r'', include('django.contrib.auth.urls')),
)
