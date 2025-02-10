# Main

Main contiene la configuración del Lumino. Es una convención que ayuda a organizar el código.

Dentro de esta carpeta, encontraremos varios archivos importantes como

## init

Este archivo indica que la carpeta debe ser tratada como un paquete de Python. Puede estar vacío, pero su presencia es necesaria para que Python reconozca el directorio como un módulo.

## settings

Este archivo contiene la configuración de Lumino, como la configuración de la base de datos, las aplicaciones instaladas, las configuraciones de seguridad, y otras opciones de configuración.

Algunas cosas a destacar:

* **login url**

Es una configuración que define la URL a la que se redirige a los usuarios no autenticados, facilitando la gestión de la autenticación en la aplicación.

```python
LOGIN_URL = 'login'
```

* **Media conf**

Estas configuraciones se utilizan para gestionar cómo se manejan los archivos multimedia y los archivos estáticos.

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [BASE_DIR / 'node_modules']
```

* **i18n**

Habilitamos el uso de i18n

```python
USE_I18N = True
```

* **Markdownify**

Es un diccionario que contiene configuraciones para el procesamiento de texto en formato Markdown. Esto permite que los usuarios ingresen utilizando bases de markdown que se convierte a HTML.

```python
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'pre'
            'strong',
            'ul'
        ]
    }
}
```

* **Crispy**

Estas configuraciones permiten utilizar Bootstrap 5 como el framework de diseño para los formularios en una app que utiliza Django Crispy Forms. Esto facilita la creación de formularios visualmente atractivos y responsivos

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

* **Email conf**

Estas configuraciones permiten a una aplicación Django enviar correos electrónicos utilizando el servidor SMTP de Brevo.

```python
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='josedomingo.rguez.rguez@gmail.com')
```

* **Certificate conf**

Define una ruta específica dentro del directorio de archivos multimedia de la aplicación para almacenar certificado de calificaciones solicitados por los estudiantes.

```python
CERTIFICATE_DIR = MEDIA_ROOT / 'certificates'
```

## Urls

Este archivo se utiliza para definir las rutas de url de lumino. Aquí es donde se mapean las urls a las vistas correspondientes, ademas de incluir las urls de las aplicaciones.

```python
urlpatterns = [
    path('', shared.views.index, name='index'), # Ruta raiz
    path('admin/', admin.site.urls),
    path('setlang/<str:langcode>/', shared.views.setlang, name='setlang'),
    path('django-rq/', include('django_rq.urls')),
    path('login/', accounts.views.user_login, name='login'),
    path('logout/', accounts.views.user_logout, name='logout'),
    path('signup/', accounts.views.user_signup, name='signup'),
    path('subjects/', include('subjects.urls')),
    path('users/', include('users.urls')),
    path('user/edit/', users.views.edit_profile, name='edit-profile'),
    path('user/leave/', users.views.leave, name='leave'),
    path('__reload__/', include('django_browser_reload.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

* **admin/** Panel de administración de Django.

* **Include**  Incluye las url del módulo correspondiente

* **__reload___** Incluye las url para el paquete django-browser-reload recargague automáticamente la página durante el desarrollo.

* **+ static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)** Esta línea agrega la configuración para servir archivos estáticos durante el desarrollo. settings.STATIC_URL es la url base para acceder a los archivos estáticos, y settings.STATIC_ROOT es el directorio donde se almacenan esos archivos.

* **if settings.DEBUG** Si la configuración de Django está en modo de depuración se agrega la configuración para servir archivos multimedia.

* **urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)** Esto permite que los archivos multimedia subidos por los usuarios sean accesibles a través de la url definida en settings.MEDIA_URL, utilizando el directorio especificado en settings.MEDIA_ROOT.

