from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import EditProfileForm
from .models import Profile


@login_required
def user_detail(request, username):
    actual_user = User.objects.get(username=username)

    return render(request, 'users/user_profile.html', dict(user=actual_user))


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.user.profile == profile:
        if request.method == 'POST':
            if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
                profile = form.save(commit=False)
                profile.save()
                messages.success(request, 'User profile has been successfully saved.')
                return redirect('users:user-detail', request.user.username)
        else:
            form = EditProfileForm(instance=profile)

        return render(request, 'users/edit.html', dict(profile=profile, form=form))

    else:
        return HttpResponseForbidden('no puedes editar esto')


@login_required
def request_certificate(request):
    pass


@login_required
def leave(request):
    if request.user.profile.role == 'S':
        user = User.objects.get(username=request.user)
        user.delete()
        messages.success(request, 'Good bye! Hope to see you soon.')
        return redirect('index')
    else:
        return HttpResponseForbidden('Eres profesor no te puedes ir')
