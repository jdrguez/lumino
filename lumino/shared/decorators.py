from django.contrib.auth import get_user_model
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


# def auth_teacher(func):
#    def wrapper(*args, **kwargs):
#        user = args[0].user
#        subject = Subject.objects.get(code=kwargs['subject_code'])
#        if user == subject.teacher:
#            return func(*args, **kwargs)
#        else:
#            return HttpResponseForbidden('no eres el profe de esta asignatura')

#    return wrapper


def get_all_emails():
    user = get_user_model()
    users = list(user.objects.all())
    emails = []
    for user in users:
        emails.append(user.email)
    return emails


def auth_user_subject(func):
    def wrapper(*args, **kwargs):
        subject = Subject.objects.get(code=kwargs['subject_code'])
        user = args[0].user
        role = user.profile.get_role()
        match role:
            case 'Student':
                if subject.students.filter(pk=user.pk).exists():
                    return func(*args, **kwargs)
                else:
                    return HttpResponseForbidden('No estás matriculado en esta asignatura')
            case 'Teacher':
                if subject.teacher == user:
                    return func(*args, **kwargs)
                else:
                    return HttpResponseForbidden('No eres el profesor de esta materia')
            case _:
                return HttpResponseForbidden('No se que pasa')

    return wrapper
