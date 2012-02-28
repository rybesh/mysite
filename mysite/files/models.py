from django.db import models
from django.contrib.auth.models import User

class Download(models.Model):
    downloader = models.ForeignKey(User, related_name='downloads')
    path = models.CharField(max_length=100)
    time_downloaded = models.DateTimeField(auto_now=True)

