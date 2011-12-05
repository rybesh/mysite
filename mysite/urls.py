from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import redirect_to, direct_to_template
from django.template import RequestContext, loader
from django import http

admin.autodiscover()

@login_required
def loggedin(request):
    if request.user.is_staff:
        return redirect('/admin/')
    for course in request.user.courses.all()[:1]:
        return redirect(course)
    return redirect('/')

def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request, {})))
handler500 = server_error 

urlpatterns = patterns('',
    url(r'^deploy/$', 'mysite.shared.views.deploy', name='shared_deploy_view'),

    (r'^$', direct_to_template, { 'template': 'bio.html' }),
    (r'^dissertation/$', direct_to_template, 
     { 'template': 'dissertation.html' }),
    (r'^dhmeetsi/$', direct_to_template, 
     { 'template': 'dhmeetsi.html' }),

    (r'^favicon.ico$', redirect_to, { 'url': '/media/img/favicon.ico' }),

    (r'^short/', include('shorturls.urls')),

    (r'^reading/', include('mysite.reading.urls')),
    (r'^talking/', include('mysite.talking.urls')),
    (r'^teaching/', include('mysite.courses.urls')),
    (r'^courses/(?P<path>.*)$', redirect_to, {'url': '/teaching/%(path)s'}),
     

    url(r'^comments/post/$', 'mysite.comments.views.post_comment', 
        name='comments_post_comment_view'),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^loggedin/$', loggedin),
    (r'', include('django.contrib.auth.urls')),
)


