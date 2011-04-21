from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect

short_domain = settings.SHORT_BASE_URL[7:-1]

special_paths = {
    '/': '',
    '/diss': 'dissertation/',
} 

class ShortURLMiddleware:
    def process_request(self, request):
        domain = request.get_host().split(':')[0]
        if domain == short_domain:
            path_prefix = 'short'
            if request.path in special_paths:
                path = special_paths[request.path]
            else:
                path = 'short%s' % request.path
            return HttpResponsePermanentRedirect('%s%s' % (
                    settings.SHORTEN_FULL_BASE_URL, path))
        else:
            return None

CONTENT_TYPES = ('text/html','application/xhtml+xml','application/xml')
HEADER_VALUE = getattr(settings, 'X_UA_COMPATIBLE', 'IE=edge,chrome=1')

class XUACompatibleMiddleware(object):
    def __init__(self, value=None):
        self.value = value
        if value is None:
            self.value = HEADER_VALUE
        if not self.value:
            raise MiddlewareNotUsed
    def process_response(self, request, response):
        content_type = response.get('Content-Type','').split(';', 1)[0].lower()
        if content_type in CONTENT_TYPES:
            if not 'X-UA-Compatible' in response:
                response['X-UA-Compatible'] = self.value
        return response

