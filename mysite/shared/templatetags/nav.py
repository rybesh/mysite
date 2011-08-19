from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def navlink(request, path, display):
    active = ''
    if request.path == path:
        active = ' class="active"' 
    return mark_safe('<a href="%s"%s>%s</a>' % (path, active, display))
