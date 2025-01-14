from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from shared.decorators import auth_user_subject, validate_type_user

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


@login_required
@auth_user_subject
def subject_detail(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    user_role = request.user.profile.get_role()
    match user_role:
        case 'Student':
            user_mark = Enrollment.objects.get(subject=subject, student=request.user).mark
        case 'Teacher':
            user_mark = None
    return render(
        request,
        'subjects/subject_detail.html',
        dict(lessons=lessons, subject=subject, mark=user_mark),
    )


@login_required
@auth_user_subject
def lesson_detail(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    return render(request, 'subjects/lesson_detail.html', dict(lesson=lesson, subject=subject))


@login_required
@validate_type_user
# @auth_teacher
@auth_user_subject
def add_lesson(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            messages.success(request, 'Lesson was successfully added.')
            return redirect(subject)
    else:
        form = AddLessonForm()
    return render(request, 'subjects/add_lesson.html', dict(form=form))


@login_required
@validate_type_user
# @auth_teacher
@auth_user_subject
def edit_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            messages.success(request, 'Changes were successfully saved.')
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'subjects/edit_lesson.html', dict(lesson=lesson, form=form))


@login_required
@validate_type_user
# @auth_teacher
@auth_user_subject
def delete_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    lesson.delete()
    messages.success(request, 'Lesson was successfully deleted.')
    return redirect('subjects:subject-detail', subject_code=subject.code)


@login_required
@validate_type_user
# @auth_teacher
@auth_user_subject
def mark_list(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    enrollments = Enrollment.objects.filter(subject=subject)
    return render(
        request, 'subjects/mark_list.html', dict(enrollments=enrollments, subject=subject)
    )


@login_required
@validate_type_user
# @auth_teacher
@auth_user_subject
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
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
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


@login_required
def enroll_subjects(request):
    if request.method == 'POST':
        if (form := AddEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.add(subject)
            messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')
        else:
            return HttpResponseForbidden('Tienes que legir al menos una!')
    else:
        form = AddEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form))


@login_required
def unenroll_subjects(request):
    if request.method == 'POST':
        if (form := UnEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.remove(subject)
            messages.warning(request, 'Successfully unenrolled from the chosen subjects.')
            return redirect('subjects:subject-list')
        else:
            return HttpResponseForbidden('Tienes que elegir al menos una!')
    else:
        form = UnEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form))
