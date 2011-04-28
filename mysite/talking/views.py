from models import *
from django.shortcuts import render_to_response, get_object_or_404

def talk(request, slug):
    o = {}
    o['talk'] = get_object_or_404(Talk, slug=slug)
    return render_to_response('talk.html', o)


