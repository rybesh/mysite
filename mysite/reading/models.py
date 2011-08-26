from django.db import models
from mysite.shared import bibutils
import json

class Text(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    zotero_id = models.CharField(max_length=16)
    zotero_json = models.TextField(blank=True, editable=False)
    citation_text = models.CharField(max_length=128, blank=True, editable=False)
    markdown = models.TextField()
    synopsis = models.TextField()
    image = models.ImageField(
        upload_to=lambda o, filename: 'images/reading/%s.png' % o.slug, 
        blank=True, null=True)
    small_image = models.ImageField(
        upload_to=lambda o, filename: 'images/reading/%s_s.png' % o.slug,
        blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=16)
    citation_key = models.CharField(max_length=32, unique=True, db_index=True)
    related_texts = models.ManyToManyField('self')
    def save(self, *args, **kwargs):
        if self.zotero_id:
            zotero_item = bibutils.load_zotero_item(self.zotero_id)
            self.zotero_json = json.dumps(zotero_item)
            self.citation_text = bibutils.zotero_item_to_text(zotero_item)
        super(Text, self).save(*args, **kwargs)
    def bibvalue(self, key):
        if self.zotero_id:
            zotero_item = json.loads(self.zotero_json)
            return zotero_item.get(key, '')
        else:
            return ''
    def title(self):
        title = self.bibvalue('title')
        shorttitle = self.bibvalue('shortTitle')
        if shorttitle is not None:
            if title and (': ' in title):
                title = title.split(': ', 1)[0]
        return title
    def subtitle(self):
        subtitle = ''
        shorttitle = self.bibvalue('shortTitle')
        if shorttitle is not None:
            title = self.bibvalue('title')
            if title and (': ' in title):
                subtitle = title.split(': ', 1)[1]
        return subtitle
    def authors(self):
        authors = []
        for creator in self.bibvalue('creators'):
            if creator['creatorType'] == 'author':
                authors.append(creator)
        return authors
    def year(self):
        return self.bibvalue('date')
    def url(self):
        return self.bibvalue('url')
    def __unicode__(self):
        return self.citation_text
    @models.permalink
    def get_absolute_url(self):
        return ('reading_text_view', (), { 
                'slug': self.slug })
    class Meta:
        ordering = [ '-created' ]

class Note(models.Model):
    text = models.ForeignKey('Text', related_name='notes')
    markdown = models.TextField()
    created = models.DateTimeField(unique=True, db_index=True)
    modified = models.DateTimeField()
    status = models.CharField(max_length=16)
    def __unicode__(self):
        return '%s %s' % (self.text.title(), self.created)
