from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def sendfile(request, path):
    response = HttpResponse(mimetype='application/pdf')
    response['X-Sendfile'] = '%s/%s' % (settings.MEDIA_ROOT, path)
    return response

