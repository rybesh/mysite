from django import template
from django.template.defaultfilters import date as datefilter
from django.utils.safestring import mark_safe
from isodate import datetime_isoformat, date_isoformat
from mysite.shared import utils

register = template.Library()

@register.filter
def timeago(datetime, format=None):
    utc_datetime = utils.naive_to_utc(datetime)
    return mark_safe(
        '<time class="timeago" pubdate="" datetime="%s">%s</time>' % (
            datetime_isoformat(utc_datetime),
            datefilter(utc_datetime, format)))

@register.filter
def dateago(date, format=None):
    return mark_safe(
        '<time class="timeago" pubdate="" datetime="%s">%s</time>' % (
            date_isoformat(date),
            datefilter(date, format)))
