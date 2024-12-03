from django.contrib import admin

# Register your models here.


from .models import Enrollment

# Register your models here.


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject']
