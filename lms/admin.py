from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)
    search_fields = ('title', 'description',)


@admin.register(Lesson)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video', 'course')
