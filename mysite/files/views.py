from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

@login_required
def sendfile(request, path):
    if path.endswith('.pdf'):
        response = HttpResponse(mimetype='application/pdf')
    elif path.endswith('.zip'):
        response = HttpResponse(mimetype='application/zip')
    else:
        raise Http404
    response['X-Sendfile'] = '%s/%s' % (settings.MEDIA_ROOT, path)
    return response

