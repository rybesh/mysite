from django import template
from django.contrib import comments
from django.contrib.comments.templatetags.comments import RenderCommentFormNode

register = template.Library()

class RenderAuthenticatedCommentFormNode(RenderCommentFormNode):
    def get_form(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            initial = None
            if 'user' in context:
                initial = { 'name': (context['user'].get_full_name() or 
                                     context['user'].username),
                            'email': context['user'].email }
            return comments.get_form()(
                ctype.get_object_for_this_type(pk=object_pk), initial=initial)
        else:
            return None

@register.tag
def render_authenticated_comment_form(parser, token):
    return RenderAuthenticatedCommentFormNode.handle_token(parser, token)
