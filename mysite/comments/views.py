from django.contrib.comments.views import comments
from django.contrib.auth.decorators import login_required

# Only accept comment POSTs from authenticated users.
@login_required
def post_comment(request, next=None, using=None):
    data = request.POST.copy()
    if not data.get('name', ''):
        data['name'] = 'anonymous'
        request.POST = data
    return comments.post_comment(request, next, using)
