from django.http import HttpResponsePermanentRedirect
from django.conf import settings

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
