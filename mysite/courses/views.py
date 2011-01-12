from models import *
from django.shortcuts import render_to_response, get_object_or_404

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
        print assignment.get_absolute_url()
    for meeting in o['meetings']:
        meeting.assignment_due = assignments.get(meeting.date, None)
    o['schedule'] = o['meetings'] + o['holidays']
    o['schedule'].sort(key=lambda x: x.date)
    return render_to_response('schedule.html', o)

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

