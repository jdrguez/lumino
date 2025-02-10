# Users 

Este módulo gestiona las funcionalidades relacionadas con los perfiles de usuario dentro del sistema. Permite a los usuarios acceder a su perfil, donde pueden ver detalles específicos de su cuenta. Además, ofrece la opción de editar su perfil, lo que les permite actualizar su información personal. Los usuarios también pueden solicitar un certificado de nostas. En conjunto, este módulo asegura que los usuarios tengan control sobre su información y su experiencia dentro de la aplicación.

## Models

En los modelos de users, hemos creado un único modelo llamado Profile, que sirve para extender el modelo de usuario que proporciona Django, permitiendo así añadir funcionalidades específicas. Esto se logra mediante una relación `OneToOneField` entre el modelo de usuario de Django y el modelo Profile creado.

```python
class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'student'
        TEACHER = 'T', 'teacher'

    role = models.CharField(
        max_length=1,
        choices=Role,
        default=Role.STUDENT,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='cache',
        default='cache/noavatar.png',
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

    def get_role(self):
        match self.role:
            case 'S':
                return 'Student'
            case 'T':
                return 'Teacher'
```

* Definimos una clase interna llama Role que nos permite asignarle un role especifico a cada perfil
* Campos del modelo:
    * **role** guarda el role del perfil
    * **user** Relacion uno a uno con el modelo user
    * **avatar** Permite agregar una imagen de perfil
    * **bio** permite al usuario agregar una biografia opcional
* Metodos:
    * **str** devuelve una representación legible del objeto,
    * **get_role** devuelve una representación legible del rol del usuario

## URLS

Dentro de las urls de user nos encontramos con las suguientes

```python
app_name = 'users'

urlpatterns = [
    path('<str:username>/', views.user_detail, name='user-detail'), # Detalle del perfil
    path('user/edit/', views.edit_profile, name='edit-profile'), # Ediar el perfil
    path('user/leave/', views.leave, name='leave'), # Dejar la plataforma
    path('certificate/', views.request_certificate, name='request-certificate'), # Solicitar el certificado de notas
]
```

## Views

Dentro de las vistas de users nos contramos con las siguientes vistas

##### **User detail**

Esta vista  muestra el perfil de un usuario específico.

```python
@login_required
def user_detail(request, username):
    actual_user = User.objects.get(username=username)

    return render(request, 'users/user_profile.html', dict(user=actual_user))
```

* `@login_required` decorador que asegura que solo los usuarios autenticados puedan acceder a esta vista.
* La función recibe el username como parámetro y utiliza `User.objects.get(username=username)` para obtener el objeto del usuario correspondiente a ese nombre de usuario. Si el usuario no existe, esto generará una excepción DoesNotExist.
* Renderizamos la plantilla pasando por el contexto el usuario correspondiente para poder acceder a su información desde la planilla.

##### **Edit profile**

Permiten que los usuarios autenticados puedan editar su perfil.

```python
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
```

* `@login_required` decorador que asegura que solo los usuarios autenticados puedan acceder a esta vista.
* Se obtiene el perfil del usuario actual utilizando `Profile.objects.get(user=request.user)` 
* Se verifica que el perfil obtenido es el mismo del usuario actual, de no ser asi se devuelve un forbidden
* Si la solicitud es POST creamos una instancia de EditProfileForm con los datos proporcionados, de ser valida se guarda el perfil actualizado y se muestra un mensaje de éxito.
* Si la solicitud no es de tipo POST, se crea una instancia del formulario con los datos del perfil existente para mostrarlo en la plantilla.

##### **Leave platform**

Permite a los usuarios que sean estudiantes dejar la plataforma. 

```python
@login_required
def leave(request):
    if request.user.profile.role == 'S':
        user = User.objects.get(username=request.user)
        user.delete()
        messages.success(request, 'Good bye! Hope to see you soon.')
        return redirect('index')
    else:
        return HttpResponseForbidden('Eres profesor no te puedes ir')
```

* `@login_required` decorador que asegura que solo los usuarios autenticados puedan acceder a esta vista.
* Comprobamos si el rol del usuario actual es estudiante, de ser asi obtenemos el user y se procede a eliminar su cuenta utilizando user.delete()
* Despues de eliminar se muestra un mensaje de èxito y redirige al landing page
* Si el usuario no es un estudiante se devuelve un error HttpResponseForbidden, indicando que no tiene permiso para eliminar su cuenta.

## Forms

Dentro de los forms de users nos contramos con el siguiente formulario.

###### **Edit Profile**

Permite a los usuarios editar su perfil, especificamente su biografia y su avatar.

```python
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'style': 'margin-bottom: 20px;',
                    'label': '',
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
```

* En la clase meta especificamos que el formulario esta basado en el modelos perfil  los campos que incluira este
* Hacemos uso de `forms.ClearableFileInput` para el campo avatar, permitiendo a los usuarios subir una nueva imagen de perfil
* Se sobrescribe el método __init__ para inicializar el formulario. Se itera sobre los campos visibles del formulario y se les asigna la clase CSS form-control, para que los campos tengan un estilo consistente.

## Templates

Dentro de las templates de users encontramos las siguientes.

##### **Edit**

Se utiliza para mostrar un formulario de edición de perfil para un usuario específico

```html
{% extends "base.html" %} 
{% block content %} 
<div class="container mt-5">
    <h1 class="text-center mb-4" style="color: #2c3e50;">Editing profile {{ user.username }}</h1>
    <div class="d-flex justify-content-center">
        <div class="card shadow-lg p-4" style="width: 50%; background-color: #ffffff; border: 1px solid #dee2e6;">
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-outline-primary btn-lg">
                            Guardar cambios 
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock content %} 
```

* `{% extends "base.html" %}` Extendemos el base de shared
* Se utiliza el bloque `{% block content %}` para definir el contenido específico de esta página.
* Se incluye el token CSRF `{% csrf_token %}` para proteger contra ataques CSRF.
* Se renderiza el formulario utilizando `{{ form.as_p }}`, lo que presenta cada campo del formulario como un párrafo.

##### **User Profile**

Se utiliza para mostrar el perfil de un usuario, incluyendo su información personal y opciones de edición.

```html
{% extends "base.html" %}
{% load thumbnail %}

{% block content %}

{% if messages %}
        
<div class="messages d-flex justify-content-end ">
    {% for message in messages  %}

        <div class="alert alert-info {{message.tags}} z-3 position-absolute opacity-75" role="alert" id="#alert-message">{{message}}</div>
    
    {% endfor %}
</div>

{% endif %}

<div class="container py-5">
  <div class="row justify-content-center mb-4">
      {% thumbnail user.profile.avatar "200x200" crop="center" format="PNG" as thumb %}
      <img src="{{thumb.url}}" alt="Avatar" class="img-fluid rounded-circle shadow-lg" style="width: 150px; height: 150px; object-fit: cover;">
      {% endthumbnail %}
  </div>

  <div class="text-center mb-4">
      <div class="d-flex justify-content-center align-items-center">
          <h1 class="mb-3" style="color: var(--dark-blue);">{{user.first_name}} {{user.last_name}}</h1> 
          {% if request.user.username == user.username %}
              <a href="{% url 'edit-profile' %}" style="color: var(--dark-blue); font-size: 1.5rem; margin-left: 10px;">
                 <i class="bi bi-pen-fill"></i>
              </a>
          {% endif %}
      </div>
      <p class="text-muted">{{user.profile.get_role}}</p>
      <p class="text-muted">{{user.email}}</p>
      <p class="lead" style="color: var(--dark-blue);">{{user.profile.bio}}</p>
  </div>

  {% if request.user.username == user.username %}
  <div class="d-flex justify-content-center mt-4">
      {% if request.user.profile.role == 'S' %}
      <a href="{% url 'users:leave' %}" class="btn btn-danger ms-3" 
         style="border-radius: 20px; padding: 0.75rem 2rem; font-weight: bold; transition: all 0.3s ease;">
         Leave the platform
      </a>
      {% endif %}
  </div>
  {% endif %}
</div>

{% endblock content %}
```

* Se utiliza `{% load thumbnail %}` para cargar la etiqueta de miniatura, que permite mostrar imágenes en un tamaño específico.
* Si hay mensajes de éxito o error se muestran en un contenedor de alertas en la parte superior derecha de la página.
* Se utiliza la etiqueta `{% thumbnail %}` para mostrar la imagen de avatar del usuario en un tamaño de 200x200 píxeles, recortada al centro y en formato PNG.
* Se muestra el nombre completo del usuario `{{user.first_name}} {{user.last_name}}``
* Se muestra un ícono de lápiz que enlaza a la página de edición del perfil.
* Se presenta el rol del usuario, su correo electrónico y una biografía breve.
* Se muestra un botón para "Leave the platform" si el rol del usuario es estudiante. Este botón permite al estudiante eliminar su cuenta.

## Context Procesor

Componente que permite agregar variables al contexto de las plantillas de Django, dentro de users tenemos.

##### **Get all subjects**

Su utilidad que recupera las materias asociadas a un usuario autenticado, dependiendo de su rol.

```python
def get_all_subjects(request) -> dict:
    if request.user.is_authenticated:
        try:
            user_role = request.user.profile.get_role()
            match user_role:
                case 'Student':
                    subjects = request.user.enrolled_subjects.all()
                case 'Teacher':
                    subjects = request.user.subjects.all()
            return {'subjects': subjects}
        except Enrollment.DoesNotExist:
            return {}
    else:
        return {}
```

* Vetificamos si el usuario esta autenticado `if request.user.is_authenticated`
* Obtenemos el role del user `get_role()`
* Utilizamos match para poder recuperar las asignaturas dependiendo del role del usuario
* Se utiliza un bloque try-except para manejar la excepción Enrollment.DoesNotExist, que podría ocurrir si no hay inscripciones asociadas al usuario
* Finalmente, se devuelve un diccionario que contiene la lista de materias `{'subjects': subjects}` si se han encontrado, o un diccionario vacío si no hay materias o si el usuario no está autenticado.

## Signals

Las signals Permite a los desarrolladores conectar funciones a eventos específicos. Dentro de users podemos encontra la siguiente.

##### **Create empty profile**

Es un receptor (handler) que se activa automáticamente después de que se guarda un nuevo usuario en la base de datos.

```python
@receiver(post_save, sender=get_user_model())
def create_empty_profile(sender, instance, created, raw, **kwargs):
    if not raw:
        if created:
            Profile.objects.create(user=instance)
```

* `@receiver` conecta la función create_empty_profile al evento post_save del modelo de usuario, que se activa cada vez que se guarda un objeto de usuario.
* Parametros
    * **sender** El modelo que envía la señal, en este caso, el modelo de usuario obtenido mediante get_user_model().
    * **instance** La instancia del modelo que se ha guardado (el usuario recién creado o actualizado).
    * **created** Un booleano que indica si se ha creado una nueva instancia (True) o si se ha actualizado una existente (False).
    * **raw** Un booleano que indica si la señal se envió antes de que se guardara la instancia en la base de datos. Si es True, significa que la instancia se está guardando de forma "cruda" y no se debe realizar ninguna acción adicional.
    * ****kwargs** Argumentos adicionales que pueden ser pasados a la función.
* Primero verifica raw sea False lo que significa que la instancia se guardo normalmente.
* Luego verifica si created es True lo que indica que se hac creado un nuevo usuario.
* Si las dos se cumplen crea un perfil asociado al usuario recien creado.

