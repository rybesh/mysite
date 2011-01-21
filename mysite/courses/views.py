from models import *
from django import forms
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def info(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('info.html', o)

def schedule(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    o['meetings'] = list(o['course'].meetings.all())
    o['holidays'] = list(o['course'].holidays.all())
    assignments = {}
    for i, assignment in enumerate(o['course'].assignments.all()):
        assignment.number = (i + 1)
        assignments[assignment.due_date] = assignment
    for meeting in o['meetings']:
        meeting.assignment_due = assignments.get(meeting.date, None)
    o['schedule'] = o['meetings'] + o['holidays']
    o['schedule'].sort(key=lambda x: x.date)
    o['user_is_authorized'] = o['course'].is_authorized(request.user)
    return render_to_response('schedule.html', o,
                              context_instance=RequestContext(request))

def guidelines(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('guidelines.html', o)

def assignments(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('assignments.html', o)

@login_required
def discussion(request, discussion_id):
    o = {}
    o['assigned'] = get_object_or_404(
        ReadingAssignment, id=discussion_id)
    o['course'] = o['assigned'].meeting.course
    if not o['course'].is_authorized(request.user):
        return HttpResponseForbidden()
    if o['assigned'].discussion_leader == request.user:
        if request.method == 'POST':
            form = DiscussionForm(request.POST)
            if form.is_valid():
                o['assigned'].discussion_questions = form.cleaned_data['questions']
                o['assigned'].save()
                messages.add_message(
                    request, messages.SUCCESS, 'Your questions have been saved.')
            else:
                print 'form not valid'
        else:
            form = DiscussionForm(
                { 'questions': o['assigned'].discussion_questions })
        o['form'] = form
    return render_to_response('discussion.html', o,
                              context_instance=RequestContext(request))

class DiscussionForm(forms.Form):
    questions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols':80}))

