# Shared

Este módulo es el encargado de crear un espacio compartido para todas las aplicaciones. En él se almacenan tanto los estilos generales como las plantillas base y sus componentes. Así mismo, existen funciones auxiliares que comparten comportamientos comunes entre aplicaciones.

## Decoradores

#### Validate type user

```python
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

```

Verificamos el rol del usuario logueado, para modificar el comportamiento de cualquier vista o función para eviar su lanzamiento si es estudiante (HTTPForbidden) y ejecutarla cuando sea profesor.

#### Auth user subject

```python

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

```

Verificamos si están matriculados en las asignaturas o si son los profesores asignados a la misma.

## Función auxiliar

#### Get all emails

```python

def get_all_emails():
    user = get_user_model()
    users = list(user.objects.all())
    emails = []
    for user in users:
        emails.append(user.email)
    return emails
```

Conseguimos todos los emails disponibles en la base de datos actual.

## Templates

#### Base

```html
{% load static %}
{% load i18n %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="{% static 'bootstrap/dist/css/bootstrap.min.css' %}">
  <link rel="stylesheet" href="{% static 'bootstrap-icons/font/bootstrap-icons.min.css' %}">
  <link rel="stylesheet" href="{% static 'shared/style.css' %}">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700&display=swap" rel="stylesheet">

  <title>Lumino</title>
</head>
<body>
  {% include "navbar.html" %}
  <div class="main-container {% if not request.user.is_authenticated %}full{% endif %}" id='mainContainer'>


    <main>

        {% block content %}





        {% endblock content %}

    </main>
    {% if request.user.is_authenticated %}
      <button class="toggle-btn" id="toggleButton"><i class="bi bi-caret-left-square-fill"></i></button>
      <sidebar id='sidebar'>{% include "componets/sidebar.html" %}</sidebar>
    {% endif %}


  </div>

  {% include "footer.html" %}
  <script type="text/javascript" src="{% static 'bootstrap/dist/js/bootstrap.bundle.min.js' %}"></script>
  <script src="{% static "shared/main.js" %}"></script>
</body>
</html>

```

Esta es la plantilla que heredan todas las demás. Muestra la estructura principal html y la inclusión de los componentes `navbar`, `footer`, `sidebar` y `user_button`. Ponemos un block content para poder llamarlos en las demás platillas y conservar el resto.
