from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.comments.models import Comment
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
        items = []
        for post in blog.posts.filter(published=True)[:10]:
            items.append(post)
            for comment in Comment.objects.for_model(post):
                items.append(comment)
        return items

    def item_title(self, item):
        if hasattr(item, 'title'):
            return item.title
        else:
            return 'Comment on %s' % item.content_object.title

    def item_description(self, item):
        if hasattr(item, 'content'):
            content = item.content
        else:
            content = item.comment
        return mark_safe(markdown2.markdown(force_unicode(content)))

    def item_author_name(self, item):
        if hasattr(item, 'display_name'):
            return item.display_name
        elif item.user_name == 'anonymous':
            return ''
        else:
            return item.name

    def item_pubdate(self, item):
        if hasattr(item, 'updated_at'):
            return item.updated_at
        else:
            return item.submit_date
