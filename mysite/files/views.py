from models import Download
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

@login_required
def sendfile(request, path):
    if path.endswith('.pdf'):
        response = HttpResponse(mimetype='application/pdf')
    elif path.endswith('.zip'):
        response = HttpResponse(mimetype='application/zip')
    elif path.endswith('.html'):
        response = HttpResponse(mimetype='text/html')
    elif path.endswith('.doc'):
        response = HttpResponse(mimetype='application/msword')
    elif path.endswith('.docx'):
        response = HttpResponse(mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    else:
        raise Http404
    Download.objects.create(downloader=request.user, path=path)
    response['X-Sendfile'] = '%s/%s' % (settings.MEDIA_ROOT, path)
    return response

