from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Subject, Lesson
from shared.decorators import validate_type_user
from .forms import AddLessonForm, EditLessonForm

@login_required
def subject_list(request):
    role = request.user.profile.get_role_display()
    match role:
        case 'student':
            subjects = Subject.objects.filter(students=request.user)
        case 'teacher':
            subjects = Subject.objects.filter(teacher=request.user)

    return render(request, 'subjects/subject_list.html', dict(subjects=subjects, total_subjects=subjects.count()))


def subject_detail(request, code):
    subject = Subject.objects.get(code=code)
    return render(request, 'subjects/subject_detail.html', dict(subject=subject))


def subject_lessons(request, code):
    subject = Subject.objects.get(code=code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject_lessons.html', dict(lessons=lessons, subject=subject))


def lesson_detail(request, code, lesson_pk):
    subject = Subject.objects.get(code=code)
    lesson = subject.lessons.get(pk = lesson_pk)
    return render(request, 'subjects/lesson_detail.html', dict(lesson=lesson, subject=subject))


@validate_type_user
def add_lesson(request, code):
    subject = Subject.objects.get(code=code)
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            return redirect(lesson)
    else:
        form = AddLessonForm()
    return render(request, 'subjects/add_lesson.html' , dict(form=form))

@validate_type_user
def edit_lesson(request, code, lesson_pk):
    subject = Subject.objects.get(code=code)
    lesson = subject.lessons.get(pk = lesson_pk)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            return redirect(lesson)
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'subjects/edit_lesson.html', dict(lesson=lesson, form=form))

@validate_type_user
def delete_lesson(request, code, lesson_pk):
    subject = Subject.objects.get(code=code)
    lesson = subject.lessons.get(pk = lesson_pk)
    lesson.delete()
    return redirect(subject)

@validate_type_user
def mark_list(request, code):
    subject = Subject.objects.get(code=code)
    students = subject.students.all()
    return render(request, 'subjects/mark_list.html', dict(students=students) )

@validate_type_user
def edit_marks():
    pass
