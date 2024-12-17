from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from shared.decorators import auth_teacher, validate_type_user

from .forms import (
    AddEnrollForm,
    AddLessonForm,
    EditLessonForm,
    EditMarkForm,
    EditMarkFormSetHelper,
    UnEnrollForm,
)
from .models import Enrollment, Subject


@login_required
def subject_list(request):
    role = request.user.profile.get_role_display()
    match role:
        case 'student':
            subjects = Subject.objects.filter(students=request.user)
        case 'teacher':
            subjects = Subject.objects.filter(teacher=request.user)

    return render(
        request,
        'subjects/subject_list.html',
        dict(subjects=subjects, total_subjects=subjects.count()),
    )


def subject_detail(request, code):
    subject = Subject.objects.get(code=code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject_detail.html', dict(lessons=lessons, subject=subject))


def lesson_detail(request, code, lesson_pk):
    subject = Subject.objects.get(code=code)
    lesson = subject.lessons.get(pk=lesson_pk)
    return render(request, 'subjects/lesson_detail.html', dict(lesson=lesson, subject=subject))


@auth_teacher
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
    return render(request, 'subjects/add_lesson.html', dict(form=form))


@validate_type_user
def edit_lesson(request, code, lesson_pk):
    subject = Subject.objects.get(code=code)
    lesson = subject.lessons.get(pk=lesson_pk)
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
    lesson = subject.lessons.get(pk=lesson_pk)
    lesson.delete()
    return redirect(subject)


@validate_type_user
def mark_list(request, code):
    subject = Subject.objects.get(code=code)
    enrollments = Enrollment.objects.filter(subject=subject)
    return render(request, 'subjects/mark_list.html', dict(enrollments=enrollments))


@validate_type_user
def edit_marks(request, subject_code):
    subject = Subject.objects.get(code=subject_code)

    """
    breadcrumbs = Breadcrumbs()
    breadcrumbs.add('My subjects', reverse('subjects:subject-list'))
    breadcrumbs.add(subject.code, reverse('subjects:subject-detail', args=[subject.code]))
    breadcrumbs.add('Marks', reverse('subjects:mark-list', args=[subject.code]))
    breadcrumbs.add('Edit marks')
    """
    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrolled_subjects.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )

    # breadcrumbs=breadcrumbs


def enroll_subjects(request):
    if request.method == 'POST':
        if (form := AddEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.add(subject)
        else:
            return HttpResponseForbidden('Tienes que legir al menos una!')
    else:
        form = AddEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form))


def unenroll_subjects(request):
    if request.method == 'POST':
        if (form := UnEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.remove(subject)
        else:
            return HttpResponseForbidden('Tienes que legir al menos una!')
    else:
        form = UnEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form))
