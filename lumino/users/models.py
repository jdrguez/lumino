from django.conf import settings
from django.db import models

# Create your models here.


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='s', on_delete=models.CASCADE
    )
