from django.contrib import admin

# Register your models here.


from .models import Enrollment, Profile

# Register your models here.


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['role']

class EnrollmentInLine(admin.TabularInline):
    model = Enrollment
    extra = 1