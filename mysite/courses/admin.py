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
    filter_horizontal = ('students',)
    def get_user_label(self, user):
        return (user.get_full_name() or user.username)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.rel.to == User:
            kwargs['queryset'] = User.objects.order_by('last_name', 'username')
        field = super(CourseAdmin, self)\
            .formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label
        return field

class MeetingAdmin(admin.ModelAdmin):
    inlines = (ReadingAssignmentInline,)
    def queryset(self, request):
        return super(MeetingAdmin, self).queryset(request)\
            .filter(course__is_archived=False)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course':
            kwargs['queryset'] = Course.objects.filter(is_archived=False)
        return super(MeetingAdmin, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)

class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }
    save_as = True
    ordering = ('-due_date',)

class ReadingAdmin(admin.ModelAdmin):
    ordering = ('citekey',)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'submitter', 'grade')
    def queryset(self, request):
        return super(SubmissionAdmin, self).queryset(request)\
            .filter(assignment__course__is_archived=False)

admin.site.register(Course, CourseAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Instructor)
