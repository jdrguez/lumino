from django.http import HttpResponse
from django.shortcuts import redirect, render
from subjects.models import Subject

from .models import Enrollment


def edit_profile():
    pass


def request_certificate():
    pass


def enroll_subjects(request):
    if request.method == 'POST':
        subject_code = request.POST.get('subject-code')
        if subject_code:
            Enrollment.objects.create(
                student=request.user,
                subject=Subject.objects.filter(code=subject_code),
            )
            return redirect('subjects:subject-list')
        else:
            return HttpResponse('Tienes que legir al menos una!')
    return render(request, 'users/add_enroll.html')


def unenroll_subjects():
    pass


def leave():
    pass
