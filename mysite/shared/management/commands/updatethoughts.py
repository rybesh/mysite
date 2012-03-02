import os
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.db import transaction
from glob import glob


class Command(NoArgsCommand):
    help = 'Updates flatpages with files from thoughts directory.'
    def handle_noargs(self, **options):
        for thought in glob(os.path.join(
                os.path.dirname(__file__), 
                '../../../../../../static/thoughts/*.md')):
            with open(thought) as f:
                lines = f.readlines()
                title = lines[0].strip()
                if not (title.startswith('<!--') and
                        title.endswith('-->')):
                    raise CommandError('No title found in %s' % thought)
                title = title[4:-4].strip()
                content = ''.join(lines[1:]).strip()
            url = '/thoughts/%s/' % thought.split('/')[-1][:-3]
            page, created = FlatPage.objects.get_or_create(url=url)
            if created:
                page.sites.add(Site.objects.get_current())
            page.title = title
            page.content = content
            page.save()
            if created:
                self.stdout.write('Created %s.\n' % url)
            else:
                self.stdout.write('Updated %s.\n' % url)
