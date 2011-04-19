from models import *
from django.shortcuts import render_to_response, get_object_or_404
from urlparse import urlparse

def text_to_obj(text):
    o = {}
    o['absolute_url'] = text.get_absolute_url()
    o['title'] = text.title()
    o['subtitle'] = text.subtitle()
    o['year'] = text.year()
    o['url'] = text.url()
    o['domain'] = urlparse(o['url']).netloc
    o['image'] = text.image
    o['small_image'] = text.small_image
    o['markdown'] = text.markdown
    o['synopsis'] = text.synopsis
    o['notes'] = text.notes.all()
    o['authors'] = [ '%s %s' % (''.join(person.first()),
                                ''.join(person.last()))
                     for person in text.authors() ]
    return o

def index(request):
    o = {}
    o['texts'] = [ text_to_obj(t) for t in Text.objects.all() ]
    return render_to_response('reading.html', o)

def text(request, slug):
    o = {}
    o['text'] = text_to_obj(get_object_or_404(Text, slug=slug))
    return render_to_response('text.html', o)
