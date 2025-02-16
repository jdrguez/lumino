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

### Componentes
Aquí procederemos a indicar cada uno de los componentes utilizamos en nuestra aplicación para generar una diversifación de las zonas html para que tengan su propio espacio para una mejor utilización y posterior modificación.

#### Navbar

```django

{% load static %}
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="{% url 'subjects:subject-list' %}" style="font-family: 'Nunito', sans-serif; font-size: 1.5rem; font-weight: bold; color: #f2c53d; text-transform: uppercase; letter-spacing: 2px; transition: color 0.3s ease;">
      <i class="bi bi-lightbulb-fill"></i>Lumino
    </a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto d-flex align-items-center"> 
        {% if user.is_authenticated %}
          <li class="nav-item">
            <button type="button" class="btn btn-secondary rounded me-3" style="background-color: #569cfd; border-style: none;">
              {{ user.profile.get_role }}
            </button>
          </li>
        {% endif %}
        <li class="nav-item">
          <a class="nav-link" href="#">
            {% if user.is_authenticated %}
              {% include "componets/user_button.html" %}
            {% endif %}
          </a>
        </li>
        
      </ul>
    </div>
  </div>
</nav>

```


##### Explicación de la Barra de Navegación  

Este código define una barra de navegación en Django usando Bootstrap, haciéndola responsiva y mostrando información del usuario si está autenticado.  

###### 1. Carga de Archivos Estáticos  
Se usa `{% load static %}` para acceder a archivos estáticos como CSS e imágenes.  

###### 2. Estructura de la Barra de Navegación  

###### Logo y Enlace Principal  
El logo y nombre de la aplicación enlazan a la lista de asignaturas, con un icono de Bootstrap Icons y estilos personalizados.  

##### Botón de Menú en Móviles  
Se añade un botón que permite colapsar o expandir el menú en pantallas pequeñas.  

##### Elementos del Menú  
La navegación usa `navbar-nav ms-auto` para alinear los elementos a la derecha.  

##### Botón con el Rol del Usuario  
Si el usuario está autenticado, se muestra su rol en un botón estilizado.  

##### Botón de Usuario  
Si el usuario ha iniciado sesión, se incluye el componente `"componets/user_button.html"`, que probablemente contenga opciones adicionales.  


#### Sidebar

```django

{% load i18n %}


<div class="container-fluid p-0 d-flex h-100" id="wrapper">
  <div id="sidebar" class="d-flex flex-column flex-shrink-0 p-3  text-white" style="width: 250px;">
      <a href="#" class="navbar-brand text-white"> <i class="bi bi-list"></i> Menu</a>
      <hr>
      <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
              <a href="{% url "subjects:subject-list" %}" class="nav-link text-white px-2">
                <i class="bi bi-house"></i> Home
              </a>
          </li>
         
          <li class="nav-item">
            <a href="#submenu3" data-bs-toggle="collapse" class="nav-link px-1 align-middle">
                <span class="ms-1 d-none d-sm-inline"> <i class="bi bi-journal-bookmark-fill"></i> {% translate "My subjects" %} </span> </a>
                <ul class="collapse nav flex-column ms-1" id="submenu3" data-bs-parent="#menu">
                    {% for subject in subjects %}
                        <li class"nav-item">
                            <a href="{% url "subjects:subject-detail" subject.code %}" class="nav-link text-white">{{subject.name}}</a>
                        </li>
                
                    {% endfor %}
                </ul>
          </li>
          <li>
            <a href="{% url 'setlang' 'en' %}?next={{ request.path }}" style="text-decoration: none;">🇺🇸</a>
            <a href="{% url 'setlang' 'es' %}?next={{ request.path }}" style="text-decoration: none;">🇪🇸</a>
        </li>
      </ul>
  </div>

</div>

```
##### Explicación de la Barra Lateral  

Este código define una **barra lateral de navegación** en Django con Bootstrap, permitiendo mostrar asignaturas dinámicamente y cambiar de idioma.  

###### 1. Estructura Principal  
La barra lateral usa `container-fluid p-0 d-flex h-100` para ocupar toda la altura y un diseño flexible.  

###### 2. Enlace de Menú  
El título "Menu" se muestra con un icono de lista y un enlace sin funcionalidad (`#`).  

###### 3. Enlaces de Navegación  
- **Inicio:** Enlace a la lista de asignaturas.  
- **Mis Asignaturas:** Se despliega dinámicamente con `collapse`.  
  - Se recorren las asignaturas (`subjects`) para generar enlaces individuales.  
- **Cambio de idioma:** Dos enlaces permiten cambiar entre inglés 🇺🇸 y español 🇪🇸.  


#### Footer

```django


<footer class="footer text-center text-lg-start">
    <div class="container">
        <div class="row">
            <div class="col-lg-4 col-md-6 mb-4">
                <h5>About Us</h5>
                <p>We are a platform dedicated to providing a complete and accessible learning experience, where students can explore various subjects, access interactive lessons, and progress at their own pace.</p>
            </div>
            <div class="col-lg-4 col-md-6 mb-4">
                <h5>Quick Links</h5>
                <ul class="list-unstyled">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Projects</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
            <div class="col-lg-4 col-md-12 mb-4">
                <h5>Connect with Us</h5>
                <div class="social-icons">
                    <a href="#" class="fab fa-facebook-f"><i class="bi bi-facebook"></i></a>
                    <a href="#" class="fab fa-twitter"><i class="bi bi-twitter-x"></i></a>
                    <a href="#" class="fab fa-instagram"><i class="bi bi-instagram"></i></a>
                    <a href="#" class="fab fa-linkedin-in"><i class="bi bi-linkedin"></i></a>
                </div>
            </div>
        </div>
    </div>
    <div class="text-center p-3">
        © 2024 Lumino. All rights reserved.
    </div>
  </footer>
  



```



##### Explicación del Pie de Página  

Este código define un **pie de página (footer)** en Bootstrap, dividido en tres secciones principales.  

##### 1. Sobre Nosotros  
Incluye una breve descripción de la plataforma, destacando su enfoque en el aprendizaje accesible.  

##### 2. Enlaces Rápidos  
Contiene una lista de enlaces de navegación a secciones clave como **Home, Services, Projects y Contact**.  

##### 3. Redes Sociales  
Muestra iconos de redes sociales con enlaces a Facebook, Twitter, Instagram y LinkedIn, usando **Bootstrap Icons**.  

###### 4. Derechos de Autor  
Se agrega un texto centrado indicando los derechos de autor del sitio web.  
