from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown2
from models import Blog

class BlogFeed(Feed):
    feed_type = Atom1Feed
    description_template = 'feeds/blog_description.html'

    def get_object(self, request, slug):
        return get_object_or_404(Blog, slug=slug)

    def title(self, blog):
        return blog.title
    
    def link(self, blog):
        return blog.get_absolute_url()

    def subtitle(self, blog):
        return 'Course blog for %s' % blog.title

    def items(self, blog):
        return blog.posts.filter(published=True)[:10]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return mark_safe(markdown2.markdown(force_unicode(post.content)))

    def item_author_name(self, post):
        return post.display_name

    def item_pubdate(self, post):
        return post.updated_at
