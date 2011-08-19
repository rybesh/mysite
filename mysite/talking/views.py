from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def talk(request, slug):
    o = {}
    o['talk'] = get_object_or_404(Talk, slug=slug)
    return render_to_response('talk.html', o,
                              context_instance=RequestContext(request))


