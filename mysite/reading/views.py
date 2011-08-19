from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from urlparse import urlparse

def text_to_obj(text):
    text.domain = urlparse(text.url()).netloc
    text.authorlist = [ '%s %s' % (''.join(person.first()),
                                   ''.join(person.last()))
                        for person in text.authors() ]
    return text

def index(request):
    o = {}
    o['texts'] = [ text_to_obj(t) for t in Text.objects.all() ]
    return render_to_response('reading.html', o,
                              context_instance=RequestContext(request))

def text(request, slug):
    o = {}
    o['text'] = text_to_obj(get_object_or_404(Text, slug=slug))
    return render_to_response('text.html', o,
                              context_instance=RequestContext(request))
