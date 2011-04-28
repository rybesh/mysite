from django.db import models

class Talk(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80, blank=True)
    date = models.DateField()
    location = models.CharField(max_length=80)
    embed = models.TextField()
    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):
        return ('talking_talk_view', (), { 'slug': self.slug })
