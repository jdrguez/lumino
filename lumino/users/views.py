from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EditProfileForm
from .models import Profile


@login_required
def user_detail(request, username):
    user = User.objects.get(username=username)

    return (request, 'users/user_profile.html', dict(user=user))


@login_required
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


@login_required
def request_certificate():
    pass


@login_required
def leave():
    pass
