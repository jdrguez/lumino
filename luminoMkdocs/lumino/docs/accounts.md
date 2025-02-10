# Accounts

 Este módulo se encarga de gestionar las credenciales de acceso de los usuarios dentro del sistema. Permite la creación, edición y eliminación de cuentas de usuario, garantizando que cada usuario tenga un perfil único. Además, se encarga de la autenticación de los usuarios, validando sus credenciales (como nombre de usuario, contraseña y email) al momento de acceder al sistema, y asegurando que solo los usuarios autorizados puedan ingresar.

## Models

Dentro de la aplicación accounts, no se definen modelos personalizados, ya que utilizamos los modelos integrados de Django para la gestión de cuentas de usuario. En lugar de crear modelos propios para usuarios, aprovechamos el modelo User de Django, que es completamente funcional y flexible para la mayoría de los casos de uso.

## Views

 Dentro de accounts.views encontramos las siguientes vistas:

##### user_login

Se encarga de la gestionar el inicio de sesión de los usuarios

* Redirigimos al usuario si este ya esta autenticado
* Cuando un usuario intenta iniciar sesión, la función verifica si la solicitud es un envío de formulario. Si es así, se valida el formulario que contiene el nombre de usuario y la contraseña.
* Si el formulario es valido, intenta autenticar el usuario con sus credenciales, de ser exitosa te redirige al subject-list, nuestro main.
*  Si las credenciales son incorrectas se mostrata el error pertinente.

```bash
def user_login(request):
    FALLBACK_REDIRECT = reverse('subjects:subject-list') 

    if request.user.is_authenticated: 
        return redirect(FALLBACK_REDIRECT) 
    login_error = False
    next = request.GET.get('next')
    if request.method == 'POST': #
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                return redirect(next or FALLBACK_REDIRECT)
            else:
                login_error = True
    else:
        form = LoginForm()
        print('hola')
    return render(
        request,
        'accounts/login.html',
        dict(form=form, login_error=login_error, next=next),
    )
```

##### user_logout

Se encarga de cerrar la sesión cuando el usuario lo solicite

* Utilizamos la función logout(request) para cerrar la sesión del usuario actual.
* Redirigimos al login

```bash
def user_logout(request):
    logout(request)
    return redirect('login')
```

##### user_singup

Gestiona el proceso de registro de nuesvos usuarios

* Si el metodo es POST y el formulario es valido creamos una instancia del SignupForm.
* Validamos que los datos del formson correctos y cumplen los requisitos.
* De ser valido lo guardamos en la base de datos.
* Se mostrara un mensaje de èxito y hace un login de forma automática.
* Si el metodo es otro diferente a POST creamos una instancia del formulario y renderizamos la plantilla del singup

```bash
def user_signup(request):
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            messages.success(request, 'Welcome to Lumino. Nice to see you!')
            login(request, user)
            return redirect('subjects:subject-list')

    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', dict(form=form))
```

## Forms

Encontramos los siguientes formularios

##### LoginForm

Formulario diseñado para manejar el inicio de seisón

* Definimos los campos, usamos el widget=forms.PasswordInput para ocultar la contraseña
* Llamamos al constructor de la clase base de forms para personalizar el nuestro
* Hacemos uso de crispy Forms para mejorar el diseño del formulario
* Con dict(novalidate=True) desactivamos la validación del formulario por parte del navegador

```bash
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Submit('login', 'Login', css_class='w-100 mt-4 mb-2'),
        )
```

### SingupForm

Formulario utilizado para registrat nuevos usuarios en la plataforma

* El formulario esta basado en el modelo de usuario.
* Definimos los campos que tendra el formulario y los onligatorios.
* La contraseña se oculta y desactivamos la ayuda para el campo de username.
* Se sobrescribe el método __init__ para inicializar el formulario y establecer que todos los campos requeridos son obligatorios.
* Hacemos uso de una validación personalizada en el campo de email para asegurarnos que este no pueda estar duplicado en la base de datos.
* Se sobrescribe el método save para establecer la contraseña del usuario de forma segura antes de guardar el objeto en la base de datos.

```bash
class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        required = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('email'),
            Submit('signup', 'Sign up', css_class='btn-info w-100 mt-2 mb-2'),
        )

    def clean_email(self):
        emails = get_all_emails()
        if self.cleaned_data['email'] in emails:
            raise ValidationError(':( Email existente')
        return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        return user
```

## Admin

Configura el modelo Profile para que sea administrado a través del panel de administración de Django.

```python
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['role']
```

* **@admin.register(Profile)** decorador que se utiliza para registrar el modelo Profile en el panel de administración de Django.

* **ProfileAdmin** esta clase hereda de admin.ModelAdmin, que es una clase base proporcionada por Django para personalizar la administración de modelos.

* **list_display** es una lista que define qué campos del modelo se mostrarán en la vista de lista del panel de administración.