import sys
import traceback
from django.core import management
from django.http import HttpResponse, HttpResponseForbidden

def deploy(request):
    if not (request.environ and 'silverlining.update' in request.environ):
        return HttpResponseForbidden()
    response = HttpResponse()
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = sys.stderr = response
    try:
        management.call_command('syncdb', noinput=True)
        print
        for app in [ 'blog', 'courses', 'reading', 'talking' ]:
            management.call_command('migrate', app, noinput=True)
            print
    except:
        traceback.print_exc(file=response)
    finally:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr
    return response
