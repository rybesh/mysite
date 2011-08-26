from models import *
from django.contrib import admin
from django.forms import ModelForm, ChoiceField
from mysite.shared import bibutils

class TextForm(ModelForm):
    zotero_id = ChoiceField(choices=bibutils.load_zotero_library())
    class Meta:
        model = Text

class TextAdmin(admin.ModelAdmin):
    form = TextForm
    readonly_fields = ('citation_text', 'zotero_json')

admin.site.register(Text, TextAdmin)
admin.site.register(Note)
