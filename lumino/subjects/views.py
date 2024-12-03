from django.contrib.auth.decorators import login_required
from .models import Subject
from django.shortcuts import redirect, render


@login_required
def subject_list(request):
    subjects =  Subject.objects.filter(user=request.user)
    return render(request, 'subjects/subject-list.html', dict(subjects = subjects))
    


def subject_detail():
    pass


def subject_lessons():
    pass


def lesson_detail():
    pass


def add_lesson():
    pass


def edit_lesson():
    pass


def delete_lesson():
    pass


def mark_list():
    pass


def edit_marks():
    pass
