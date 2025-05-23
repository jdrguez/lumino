from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'student'
        TEACHER = 'T', 'teacher'

    role = models.CharField(
        max_length=1,
        choices=Role,
        default=Role.STUDENT,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='cache',
        default='cache/noavatar.png',
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

    def get_role(self):
        match self.role:
            case 'S':
                return 'Student'
            case 'T':
                return 'Teacher'
