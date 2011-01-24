from django import forms
from django.utils.safestring import mark_safe
from django.contrib.comments.forms import CommentForm, COMMENT_MAX_LENGTH
from django.utils.translation import ungettext, ugettext_lazy as _

class AuthenticatedCommentForm(CommentForm):
    name = forms.CharField(
        label=_("Name"), max_length=50, required=False,
        help_text='Leave this blank to comment anonymously.')
    email = forms.EmailField(widget=forms.HiddenInput)
    url = forms.URLField(widget=forms.HiddenInput, required=False)
    comment = forms.CharField(
        label=_('Comment'), widget=forms.Textarea, max_length=COMMENT_MAX_LENGTH,
        help_text=mark_safe('You may use <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> syntax but not HTML tags.'))
