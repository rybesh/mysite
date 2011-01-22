from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=80)
    def __unicode__(self):
        return self.title

class Post(models.Model):
    blog = models.ForeignKey('Blog', related_name='posts')
    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def is_anonymous(self):
        return (len(self.display_name.strip()) == 0)
    def updated_after_published(self):
        if not self.published:
            return False
        return ((self.updated_at - self.published_at).seconds > 60)
    @models.permalink
    def get_absolute_url(self):
        return ('course_blog_post_view', (), { 
                'slug': self.blog.slug, 
                'post_slug': self.slug }) 
    def get_edit_url(self):
        return reverse('course_blog_edit_post_view', kwargs={ 
                'slug': self.blog.slug, 
                'post_slug': self.slug })
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ('-published_at', '-updated_at')

class Tag(models.Model):
    post = models.ForeignKey('Post', related_name='tags')
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name


