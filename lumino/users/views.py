from django.http import HttpResponse
from django.shortcuts import redirect, render
from subjects.models import Subject
from django.contrib.auth.models import User
from .models import Enrollment, Profile
from django.urls import reverse
from .forms import EditProfileForm

def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect(reverse('user-detail', kwargs={'username': username}))
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit.html', dict(profile=profile, form=form))


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
