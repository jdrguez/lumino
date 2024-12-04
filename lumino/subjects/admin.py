from django.contrib import admin
from users.admin import EnrollmentInLine
from .models import Subject, Lesson

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInLine]
    list_display = ['name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
