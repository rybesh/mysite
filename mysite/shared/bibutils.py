from StringIO import StringIO
from django.conf import settings
from django.utils.safestring import mark_safe
from pybtex.backends import html, plaintext
from pybtex.database import BibliographyData
from pybtex.database.input import bibtex as bibtex_in
from pybtex.database.output import bibtex as bibtex_out
from pybtex.style.formatting import custom
from urllib import urlopen
from xml.etree.ElementTree import ElementTree
import json

def parse(bib):
    parser = bibtex_in.Parser()
    return parser.parse_stream(StringIO(bib))

def parse_file(filename):
    parser = bibtex_in.Parser()
    return parser.parse_file(filename)

def extract(bibdata, citekey):
    if not citekey in bibdata.entries:
        return None
    entries = { citekey: bibdata.entries[citekey] }
    writer = bibtex_out.Writer()
    output = StringIO()
    writer.write_stream(BibliographyData(entries), output)
    return output.getvalue()

def citekeys(bib):
    return parse(bib).entries.keys()

def format(bib, backend):
    style = custom.Style()
    return [ 
        formatted_entry.text.render(backend) for formatted_entry in 
        style.format_entries(parse(bib).entries) ]

def format_bibtex_as_html(bib):
    return mark_safe(u'<br>'.join(format(bib, html.Backend())))

def format_bibtex_as_text(bib):
    return u'\n'.join(format(bib, plaintext.Backend()))

def format_zotero_as_html(zotero_item_id):
    return mark_safe(urlopen(
            'https://api.zotero.org/groups/%s/items/%s?format=bib' 
            % (settings.ZOTERO_GROUP_ID, zotero_item_id)).read().replace(
            '<?xml version="1.0"?>', ''))

def zotero_item_to_text(item):
    return '%s (%s)' % (item['title'],
                        ', '.join([ '%s %s' % (c['firstName'], c['lastName']) 
                                    for c in item['creators'] ]))


def format_zotero_as_text(zotero_item_id):
    return zotero_item_to_text(load_zotero_item(zotero_item_id))

def load_zotero_item(zotero_item_id):
    tree = ElementTree()
    tree.parse(urlopen(
            'https://api.zotero.org/groups/%s/items/%s?content=json' 
            % (settings.ZOTERO_GROUP_ID, zotero_item_id)))
    return json.loads(tree.find('{http://www.w3.org/2005/Atom}content').text)

def load_zotero_atom(uri):
    tree = ElementTree()
    tree.parse(urlopen(uri))
    library = []
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        key = entry.find('{http://zotero.org/ns/api}key').text
        content = entry.find('{http://www.w3.org/2005/Atom}content').text
        library.append((key, zotero_item_to_text(json.loads(content))))
    for link in tree.findall('{http://www.w3.org/2005/Atom}link'):
        if link.attrib.get('rel', None) == 'next':
            library.extend(load_zotero_atom(link.attrib['href']))
            break
    return library

def load_zotero_library():
    return load_zotero_atom(
        'https://api.zotero.org/groups/%s/items' % settings.ZOTERO_GROUP_ID
        + '?content=json&order=title&limit=99')

