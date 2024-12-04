from django.contrib import admin

from .models import Enrollment, Lesson, Subject

# Register your models here.


class EnrollmentInLine(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInLine]
    list_display = ['name']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject']
