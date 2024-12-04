from django.http import HttpResponseForbidden
from subjects.models import Subject


def validate_type_user(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        role = user.profile.get_role_display()

        match role:
            case 'student':
                return HttpResponseForbidden('No puedes editar esto')
            case 'teacher':
                return func(*args, **kwargs)

    return wrapper


def auth_teacher(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        subject = Subject.objects.get(code=kwargs['code'])
        if user == subject.teacher:
            return func(*args, **kwargs)
        else:
            return HttpResponseForbidden('no eres el profe de esta asignatura')

    return wrapper
