from models import *
from django.contrib import admin

class HolidayInline(admin.StackedInline):
    model = Holiday
    extra = 0

class ReadingAssignmentInline(admin.StackedInline):
    model = ReadingAssignment
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    inlines = (HolidayInline,)
    prepopulated_fields = { 'slug': ('number',) }

class MeetingAdmin(admin.ModelAdmin):
    inlines = (ReadingAssignmentInline,)

class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }

class ReadingAdmin(admin.ModelAdmin):
    ordering = ('citekey',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Instructor)
