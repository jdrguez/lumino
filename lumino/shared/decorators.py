from django.http import HttpResponseForbidden



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