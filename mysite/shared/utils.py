from pytz import timezone, utc
from django.conf import settings

def naive_to_utc(naive_datetime, timezone_string=None):
    '''Converts a naive datetime (such as Django returns from DateTimeFields) 
    to an timezone-aware UTC datetime. It will be assumed that the naive 
    datetime refers to a time in the timezone specified by settings.TIME_ZONE, 
    unless a timezone string (e.g. "America/Los_Angeles") is provided.'''
    if naive_datetime.tzinfo is not None:
        raise TypeError('datetime is not naive: %s' % naive_datetime)
    if timezone_string is None:
        timezone_string = settings.TIME_ZONE
    tz = timezone(timezone_string)
    return tz.normalize(tz.localize(naive_datetime)).astimezone(utc)

def truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
