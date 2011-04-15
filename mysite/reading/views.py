from models import *
from django.shortcuts import render_to_response, get_object_or_404
from urlparse import urlparse

def text(request, slug):
    o = {}
    o['text'] = {}
    text = get_object_or_404(Text, slug=slug)
    o['text']['title'] = text.title()
    o['text']['subtitle'] = text.subtitle()
    o['text']['year'] = text.year()
    o['text']['url'] = text.url()
    o['text']['domain'] = urlparse(o['text']['url']).netloc
    o['text']['image'] = text.image
    o['text']['markdown'] = text.markdown
    o['text']['notes'] = text.notes.all()
    o['text']['authors'] = [ '%s %s' % (''.join(person.first()),
                                        ''.join(person.last()))
                             for person in text.authors() ]
    return render_to_response('text.html', o)
