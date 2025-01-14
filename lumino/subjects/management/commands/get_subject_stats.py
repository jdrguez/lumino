from django.core.management.base import BaseCommand, CommandError
from subjects.models import Enrollment, Subject


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('subjects', nargs='*', type=int, default=-1)

    def handle(self, *args, **options):
        for subject in Subject.objects.all():
            try:
                enrollments = Enrollment.objects.filter(subject=subject)

            except Subject.DoesNotExist:
                raise CommandError(f'Subject {subject.pk} does not exist')

            students_with_marks = 0
            media_marks = 0

            for enrollment in enrollments:
                mark = enrollment.mark
                if mark:
                    students_with_marks += 1
                    media_marks += mark
                if media_marks > 0:
                    media_marks = media_marks / students_with_marks

            self.stdout.write(self.style.SUCCESS(f'{enrollment.subject.code}: {media_marks:.2f}'))
