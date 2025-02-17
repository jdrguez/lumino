# Lumino

Bienvenido a la documentación oficial de **Lumino**, un proyecto desarrollado con Django. Aquí encontrarás información detallada sobre la arquitectura, funcionalidades y módulos que componen esta plataforma.

## Introducción

Lumino es una plataforma diseñada para la gestión de un centro estudiantil, donde alumnos y profesores pueden interactuar a través de asignaturas y lecciones propias de la misma. Los profesores pueden calificar a los alumnos, quienes a su vez pueden visualizar sus notas. Además, cada usuario cuenta con un perfil propio, y los profesores tienen la capacidad de subir u actualizar las clases de sus asignaturas.

## Estructura del Proyecto

El proyecto está dividido en cuatro aplicaciones principales, cada una con una función específica dentro del sistema:

1. **Accounts**: Se encarga de gestionar las credenciales de acceso de los usuarios, permitiendo la creación, edición y eliminación de cuentas, así como la autenticación y autorización en el sistema.
2. **Subjects**: Organiza y clasifica las Asignaturas y las lecciones de conocimiento impartidas por un profesor.
3. **Users**: Administra los perfiles de los usuarios, incluyendo roles dentro de la aplicación de cada uno.
4. **Shared**: Permite compartir recursos, archivos o datos entre las diferentes aplicaciones dentro de Lumino.

## Instalación y Configuración

Para ejecutar Lumino en tu entorno local, sigue estos pasos:

```bash
# Clonar el repositorio
git clone https://github.com/jdrguez/lumino/
cd lumino

# Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate

# Crear un superusuario
python manage.py createsuperuser

# Ejecutar el servidor
django-admin runserver
```

## Uso del Proyecto

### Acceso a la Plataforma

Una vez que el servidor esté en ejecución, puedes acceder a la plataforma a través de:

```
http://127.0.0.1:8000/
```

El panel de administración estará disponible en:

```
http://127.0.0.1:8000/admin/
```

## Contacto

Para dudas o sugerencias, puedes ponerte en contacto con el equipo de desarrollo a través de [correo/contacto].
