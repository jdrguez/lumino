from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Subject


@login_required
def subject_list(request):
    role = request.user.profile.get_role_display()
    match role:
        case 'student':
            subjects = Subject.objects.filter(students=request.user)
        case 'teacher':
            subjects = Subject.objects.filter(teacher=request.user)

    return render(request, 'subjects/subject-list.html', dict(subjects=subjects, total_subjects=subjects.count()))


def subject_detail():
    pass


def subject_lessons(request, code):
    subject = Subject.objects.filter(code=code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject_deiail.html', dict(lessons=lessons))


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
