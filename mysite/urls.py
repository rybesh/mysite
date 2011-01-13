from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import redirect_to

admin.autodiscover()

@login_required
def loggedin(request):
    if request.user.is_staff:
        return redirect('/admin/')
    for course in request.user.courses.all()[:1]:
        return redirect(course)
    return redirect('/')

urlpatterns = patterns('',
    (r'^$', redirect_to, { 
            'url': 'http://people.ischool.berkeley.edu/~ryanshaw/wordpress/bio/',
            'permanent': False }),
    (r'^favicon.ico$', 'django.views.generic.simple.redirect_to', 
     { 'url': '/media/img/favicon.ico' }),
    (r'^courses/', include('mysite.courses.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^loggedin/$', loggedin),
    (r'', include('django.contrib.auth.urls')),
)
