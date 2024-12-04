from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EditProfileForm
from .models import Profile


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


def leave():
    pass
