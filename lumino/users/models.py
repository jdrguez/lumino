from django.conf import settings
from django.db import models

# Create your models here.


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='enrollments',
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        related_name='enrollments',
        on_delete=models.CASCADE,
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.student} {self.subject} enrolled at {self.enrolled_at}'


class Profile(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ROLES_CHOICES = {
        STUDENT: 'student',
        TEACHER: 'teacher',
    }
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=1,
        choices=ROLES_CHOICES,
        default=STUDENT,
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='avatars',
        default='avatars/noavatar.png',
    )
