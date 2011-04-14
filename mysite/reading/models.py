from django.db import models
from mysite.shared import bibutils

class Text(models.Model):
    slug = models.SlugField(unique=True, max_length=80)
    bibtex = models.TextField()
    markdown = models.TextField()
    image = models.ImageField(
        upload_to=lambda o, filename: 'images/reading/%s.png' % o.slug)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=16)
    citation_key = models.CharField(max_length=32, unique=True)
    related_texts = models.ManyToManyField('self')
    def bibvalue(self, key):
        entries = bibutils.parse(self.bibtex).entries
        value = entries[self.citation_key].fields.get(key, None)
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
    def url(self):
        return self.bibvalue('url')
    def __unicode__(self):
        return self.title()

class Note(models.Model):
    text = models.ForeignKey('Text')
    markdown = models.TextField()
    created = models.DateTimeField(unique=True)
    modified = models.DateTimeField()
    status = models.CharField(max_length=16)
    def __unicode__(self):
        return '%s %s' % (self.text.title(), self.created)
