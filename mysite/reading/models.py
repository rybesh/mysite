from django.db import models
from mysite.shared import bibutils

class Text(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    bibtex = models.TextField()
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
    def bibvalue(self, key):
        entry = bibutils.parse(self.bibtex).entries[self.citation_key]
        if key in ['author']:
            value = entry.persons.get(key, None)
        else:
            value = entry.fields.get(key, None)
            if value is not None:
                value = value.strip('{ }')
        return value
    def title(self):
        title = self.bibvalue('title')
        shorttitle = self.bibvalue('shorttitle')
        if shorttitle is not None:
            if title and (': ' in title):
                title = title.split(': ', 1)[0]
        return title
    def subtitle(self):
        subtitle = ''
        shorttitle = self.bibvalue('shorttitle')
        if shorttitle is not None:
            title = self.bibvalue('title')
            if title and (': ' in title):
                subtitle = title.split(': ', 1)[1]
        return subtitle
    def authors(self):
        return self.bibvalue('author')
    def year(self):
        return self.bibvalue('year')
    def url(self):
        return self.bibvalue('url')
    def __unicode__(self):
        return self.title()
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
