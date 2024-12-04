from django.shortcuts import redirect, render

# Create your views here.


def index(request):
    if request.user:
        return redirect('subjects:subject-list')
    return render(request, 'landing.html')
