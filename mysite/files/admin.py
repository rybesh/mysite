from models import Download
from django.contrib import admin

class DownloadAdmin(admin.ModelAdmin):
    list_display = ('downloader', 'path', 'time_downloaded')
    readonly_fields = ('downloader', 'path', 'time_downloaded')

admin.site.register(Download, DownloadAdmin)
