from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import translation

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')
    return render(request, 'landing.html')


def setlang(request, langcode):
    next = request.GET.get('next', '/')
    translation.activate(langcode)
    response = redirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langcode)
    return response
