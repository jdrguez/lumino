from django.conf import settings
from django.db import models
from django.urls import reverse


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subjects',
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='subjects.Enrollment',
        related_name='enrolled_subjects',
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}: {self.name}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'code': self.code})


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(
        Subject,
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'subjects:lesson-detail', kwargs={'code': self.subject.code, 'lesson_pk': self.pk}
        )


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
    mark = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.student} {self.subject} enrolled at {self.enrolled_at}'
