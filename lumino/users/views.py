from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EditProfileForm
from .models import Profile

USER = get_user_model()


@login_required
def user_detail(request, username):
    actual_user = USER.objects.get(username=username)

    return (request, 'users/user_profile.html', dict(user=actual_user))


@login_required
def edit_profile(request, username):
    user = USER.objects.get(username=username)
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
