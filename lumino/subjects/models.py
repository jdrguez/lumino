from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='subjects', on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Enrollment',
        through_fields=('student', 'subject'),
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}: {self.name}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'subject_pk': self.pk})


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(
        'subjects.Subject',
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subjects:lesson-detail', kwargs={'lesson_pk': self.pk})
