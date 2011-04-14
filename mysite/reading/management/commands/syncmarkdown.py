from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.template.defaultfilters import slugify
from mysite.reading.models import Text, Note
from mysite.shared import bibutils

DATETIME_FMT = '%d %B %Y, %H:%M'

class Command(BaseCommand):
    args = '<markdown_file> <bibtex_file>'
    help = 'Sync from local Markdown file to server.'
    @transaction.commit_on_success
    def handle(self, *args, **options):
        def update_metadata(o, metadata):
            o.created = datetime.strptime(metadata['Created'], DATETIME_FMT)
            o.modified = datetime.strptime(metadata['Modified'], DATETIME_FMT)
            o.status = metadata['Status']
        def create_or_update_text(metadata, markdown):
            if not 'Citation Key' in metadata:
                raise CommandError(
                    'text metadata is missing a citation key:\n%s' % metadata)
            citekey = metadata['Citation Key']
            try:
                text = Text.objects.get(citation_key=citekey)
            except Text.DoesNotExist:
                text = Text(citation_key=citekey)
            update_metadata(text, metadata)
            text.markdown = '\n'.join(markdown)
            text.bibtex = bibutils.extract(bib, citekey)
            if text.bibtex is None:
                raise CommandError('No citekey %s in %s' % (citekey, args[1]))
            text.slug = slugify(text.title())
            text.save()
            if 'Related' in metadata:
                for citekey in metadata['Related'].split(','):
                    text.related_texts.add(
                        Text.objects.get(citation_key=citekey))
            return text 
        def create_or_update_note(text, metadata, markdown):
            created = datetime.strptime(metadata['Created'], DATETIME_FMT)
            try:
                note = Note.objects.get(created=created)
            except Note.DoesNotExist:
                note = Note()
            update_metadata(note, metadata)
            note.text = text
            note.markdown = '\n'.join(markdown)
            note.save()
        bib = bibutils.parse_file(args[1])
        with open(args[0]) as f:
            state = 'start'
            skip = True
            metadata = markdown = text = note = None
            for line in f:
                if skip:
                    skip = False
                    continue
                line = line.strip()
                if state == 'start':
                    if line.startswith('# '):
                        state = 'text_metadata'
                        metadata = {}
                        skip = True
                    elif line.startswith('## '):
                        state = 'note_metadata'
                        metadata = {}
                        skip = True
                elif state.endswith('_metadata'):
                    if ':' in line:
                        key, value = [ x.strip() for x in line.split(':', 1) ]
                        metadata[key] = value
                    else:
                        state = state.replace('metadata', 'markdown')
                        markdown = []
                elif state == 'text_markdown':
                    if line == '----':
                        markdown = markdown[:-1]
                        text = create_or_update_text(metadata, markdown)
                        state = 'start'
                    else:
                        markdown.append(line)
                elif state == 'note_markdown':
                    if line == '----':
                        markdown = markdown[:-1]
                        create_or_update_note(text, metadata, markdown)
                        state = 'start'
                    else:
                        markdown.append(line)
            if state == 'text_markdown':
                create_or_update_text(metadata, markdown)
            elif state == 'note_markdown':
                create_or_update_note(text, metadata, markdown)

                    
                        
                    
        
