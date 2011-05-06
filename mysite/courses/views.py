from models import *
from mysite.blog.models import Blog, Post
from django import forms
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Count
from django.utils.safestring import mark_safe
from zipfile import ZipFile, BadZipfile
from StringIO import StringIO
import datetime
import csv

def info(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('info.html', o,
                              context_instance=RequestContext(request))

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
    o['in_flux'] = False
    for meeting in o['meetings']:
        meeting.assignment_due = assignments.get(meeting.date, None)
        if meeting.is_tentative: o['in_flux'] = True
    
    o['schedule'] = o['meetings'] + o['holidays']
    o['schedule'].sort(key=lambda x: x.date)
    today = datetime.date.today()
    for item in o['schedule']:
        if item.date >= today:
            item.next = True
            break
    o['user_is_authorized'] = o['course'].is_authorized(request.user)
    return render_to_response('schedule.html', o,
                              context_instance=RequestContext(request))

def guidelines(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('guidelines.html', o,
                              context_instance=RequestContext(request))

def assignments(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    return render_to_response('assignments.html', o,
                              context_instance=RequestContext(request))

class DiscussionForm(forms.Form):
    questions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols':80}),
        help_text=mark_safe('You may use <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> syntax but not HTML tags.'))

@login_required
def discussion(request, discussion_id):
    o = {}
    o['assigned'] = get_object_or_404(
        ReadingAssignment, id=discussion_id)
    o['course'] = o['assigned'].meeting.course
    if not o['course'].is_authorized(request.user):
        return HttpResponseForbidden()
    return render_to_response('discussion.html', o,
                              context_instance=RequestContext(request))

@login_required
def edit_discussion(request, discussion_id):
    o = {}
    o['assigned'] = get_object_or_404(
        ReadingAssignment, id=discussion_id)
    if not o['assigned'].discussion_leader == request.user:
        return HttpResponseForbidden()
    o['course'] = o['assigned'].meeting.course
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            o['assigned'].discussion_questions = form.cleaned_data['questions']
            o['assigned'].save()
            messages.add_message(
                request, messages.SUCCESS, 'Your questions have been saved.')
            return redirect(o['assigned'].get_absolute_url())
    else:
        form = DiscussionForm(
            { 'questions': o['assigned'].discussion_questions })
        o['form'] = form
        return render_to_response('edit_discussion.html', o,
                                  context_instance=RequestContext(request))

class SubmissionForm(forms.Form):
    zipfile = forms.FileField(help_text='Please upload a single zip archive containing all the required files for this assignment.')

@login_required
def submit_assignment(request, assignment_id):
    o = {}
    o['assignment'] = get_object_or_404(Assignment, id=assignment_id)
    if not (o['assignment'].is_handed_out and 
            o['assignment'].is_submitted_online):
        return HttpResponseNotFound()
    o['course'] = o['assignment'].course
    if not o['course'].is_authorized(request.user):
        return HttpResponseForbidden()
    submission = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            zipfile = request.FILES['zipfile']
            try:
                archive = ZipFile(zipfile)
                submission, new = o['assignment'].submissions.get_or_create(submitter=request.user)
                if not new:
                    submission.zipfile.delete(save=False)
                submission.zipfile = zipfile
                submission.save()
                messages.success(request, 'Your zip archive was successfully uploaded.')
            except BadZipfile:
                messages.error(request, 'The file %s is not a valid zip archive.' % zipfile.name)
    else:
        submitter=request.user.username
        if request.user.is_superuser and 'username' in request.GET:
            submitter = request.GET['username']
        try:
            submission = o['assignment'].submissions.get(
                submitter__username=submitter)
        except Submission.DoesNotExist:
            pass
        form = SubmissionForm()
    if submission:
        try:
            o['files'] = ZipFile(submission.zipfile).namelist()
            o['zipfile_url'] = submission.zipfile.url
        except:
            pass
    o['form'] = form
    return render_to_response('submit_assignment.html', o,
                              context_instance=RequestContext(request))

def get_current_course(slug):
    courses = list(Course.objects.filter(slug=slug).order_by('id'))
    if len(courses) == 0:
        raise Course.DoesNotExist
    return courses[-1]

def blog(request, slug, post_slug=None):
    o = {}
    o['blog'] = get_object_or_404(Blog, slug=slug)
    o['domain'] = Site.objects.get_current().domain
    o['course'] = get_current_course(slug)
    o['user_is_authorized'] = o['course'].is_authorized(request.user)
    if post_slug:
        posts = o['blog'].posts.filter(slug=post_slug, published=True)
        if len(posts) == 0:
            raise Http404
        o['show_comment_form'] = True
        o['next'] = posts[0].get_absolute_url()
    elif 'mine' in request.GET:
        posts = o['blog'].posts.filter(author=request.user).order_by('-updated_at')
    else:
        posts = o['blog'].posts.filter(published=True)
    paginator = Paginator(posts, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        o['page'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        o['page'] = paginator.page(paginator.num_pages)
    return render_to_response('blog.html', o,
                              context_instance=RequestContext(request))

def median(pool):
    copy = sorted(pool)
    size = len(copy)
    if size % 2 == 1:
        return copy[(size - 1) / 2]
    else:
        return (copy[size/2 - 1] + copy[size/2]) / 2

def grades_csv(course):
    assignments = course.assignments.filter(is_graded=True)
    table = [ ['Name'] + [ a.title for a in assignments ] ] 
    for s in course.students.filter(is_active=True):
        row = [s.get_full_name()]
        for a in assignments:
            try:
                row.append(a.submissions.get(submitter=s).grade)
            except Submission.DoesNotExist:
                row.append('')
        table.append(row)
    buf = StringIO() 
    csv.writer(buf).writerows(table)
    return HttpResponse(buf.getvalue(), 'text/csv')

@login_required
def dashboard(request, slug, year, semester):
    o = {}
    o['course'] = get_object_or_404(
        Course, slug=slug, year=year, semester=semester)
    if request.user.is_superuser:
        if 'username' in request.GET:
            o['student'] = get_object_or_404(
                User, username=request.GET['username'])
        else:
            return grades_csv(o['course'])
    elif o['course'].has_student(request.user):
        o['student'] = request.user
    else:
        return HttpResponseForbidden()
    students = o['course'].students\
        .filter(is_active=True)\
        .values_list('username', flat=True)
    counts = {}
    def setdefault(username):
        return counts.setdefault(username, { 
                'discussion_count': 0, 'post_count': 0, 'comment_count': 0 })
    for leader in ReadingAssignment.objects\
            .filter(meeting__course=o['course'])\
            .values_list('discussion_leader__username', flat=True):
        if leader in students:
            setdefault(leader)['discussion_count'] += 1
    o['discussion_count'] = setdefault(o['student'].username)['discussion_count']
    o['discussion_median'] = median([ v['discussion_count'] for v in counts.values() ])
    blog = Blog.objects.get(slug=slug)
    if blog:
        o['blog_metrics'] = True
        date_range = o['course'].get_date_range()
        for poster in blog.posts\
            .filter(published_at__range=date_range)\
            .values_list('author__username', flat=True):
            if poster in students:
                setdefault(poster)['post_count'] += 1
        for commenter in Comment.objects\
            .filter(submit_date__range=date_range)\
            .values_list('user__username', flat=True):
            if commenter in students:
                setdefault(commenter)['comment_count'] += 1
        o['post_count'] = setdefault(o['student'].username)['post_count']
        o['post_median'] = median([ v['post_count'] for v in counts.values() ])
        o['comment_count'] = setdefault(o['student'].username)['comment_count']
        o['comment_median'] = median([ v['comment_count'] for v in counts.values() ])
    o['assignments'] = []
    for assignment in o['course'].assignments.filter(is_graded=True):
        grades = {}
        comments = ''
        for submission in assignment.submissions.all():
            if submission.submitter.username in students:
                grades[submission.submitter.username] = submission.grade
            if submission.submitter == o['student']:
                comments = submission.comments
        o['assignments'].append({
                'title': assignment.title,
                'points': assignment.points,
                'grade': grades.get(o['student'].username, ''),
                'median': median(grades.values()),
                'comments': comments })
    return render_to_response('dashboard.html', o,
                              context_instance=RequestContext(request))

class BlogPostForm(forms.Form):
    title = forms.CharField(max_length=80)
    slug = forms.CharField(max_length=50)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols':80}))
    display_name = forms.CharField(required=False, max_length=32)

@login_required
def edit_post(request, slug, post_slug=None):
    o = {}
    o['blog'] = get_object_or_404(Blog, slug=slug)
    o['course'] = get_current_course(slug)
    if post_slug: # editing existing post
        post = o['blog'].posts.get(slug=post_slug)
        if not post.author == request.user:
            return HttpResponseForbidden()
        if request.method == 'POST':
            form = BlogPostForm(request.POST)
            if form.is_valid():
                post.content = form.cleaned_data['content']
                post.display_name = form.cleaned_data['display_name']
                if post.published:
                    message = 'Your post has been updated.'
                    next = post.get_absolute_url()
                else:
                    post.title = form.cleaned_data['title']
                    post.slug = form.cleaned_data['slug']
                    if 'publish' in request.POST:
                        post.published = True
                        post.published_at = datetime.datetime.now()
                        message = 'Your post has been published.'
                        next = post.get_absolute_url()
                    else:
                        message = 'Your draft has been saved.'
                        next = post.get_edit_url()
                post.save()
                messages.add_message(request, messages.SUCCESS, message)
                return redirect(next)
        else:
            form = BlogPostForm({ 'title': post.title,
                                  'slug': post.slug,
                                  'content': post.content,
                                  'display_name': post.display_name })
            if post.published:
                o['post_published'] = True
                for field in ['title', 'slug']:
                    form.fields[field].widget.attrs['readonly'] = True
    else:         # creating new post
        if not o['course'].is_authorized(request.user):
            return HttpResponseForbidden()
        if request.method == 'POST':
            form = BlogPostForm(request.POST)
            if form.is_valid():
                post = Post(blog=o['blog'], author=request.user)
                post.title = form.cleaned_data['title']
                post.slug = form.cleaned_data['slug']
                post.content = form.cleaned_data['content']
                post.display_name = form.cleaned_data['display_name']
                if 'publish' in request.POST:
                    post.published = True
                    post.published_at = datetime.datetime.now()
                    message = 'Your post has been published.'
                    next = post.get_absolute_url()
                else:
                    message = 'Your draft has been saved.'
                    next = post.get_edit_url()
                post.save()
                messages.add_message(request, messages.SUCCESS, message)
                return redirect(next)
        else:
            form = BlogPostForm(initial={ 
                    'display_name': (request.user.get_full_name() or 
                                     request.user.username) })
    o['form'] = form
    return render_to_response('edit_post.html', o,
                              context_instance=RequestContext(request))
        
                
            

