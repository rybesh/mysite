from django.contrib.comments.models import Comment
from forms import AuthenticatedCommentForm

def get_model():
    return Comment

def get_form():
    return AuthenticatedCommentForm
