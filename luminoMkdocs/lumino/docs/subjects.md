# Subjects

Este módulo maneja las funcionalidades relacionadas con la gestión académica. Permite administrar asignaturas, lecciones y matrículas de los usuarios. Además, facilita el registro y consulta de calificaciones, asegurando un seguimiento detallada del rendimiento academico. También ofrece opciones para la actualizacion de información académica y la generacion de certificados. En conjunto, este módulo garantiza una gestión eficiente y estructurada del proceso educativo dentro de la aplicación.

## Models

Dentro de los modelos de subjects podemos encontrar:

##### Subject

```python

class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subjects',
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='subjects.Enrollment',
        related_name='enrolled_subjects',
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}: {self.name}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'subject_code': self.code})


```

- Campos del modelo
  - **code** Es el código de cada subject, encargado de indentificar, de manera única, cada una.
  - **name** Nombre de la subject
  - **teacher** Es una relación 1:N, entre el profesor y la asignatura asignada.
  - **students** Es una relación N:M que comprende un modelo intermedio, llamado enrollment (detallado más abajo).
- Métodos del modelo
  - **str** Devuelve una representación legible del objeto.
  - **get_absolute_url** Devuelve la url absoluta del objeto en cuestión.
- Class Meta
  - **Ordering** Indica la manera de ordenar cada objeto al salir de la base de datos.

##### Lesson

```python

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(
        Subject,
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'subjects:lesson-detail', kwargs={'subject_code': self.subject.code, 'lesson_pk': self.pk}
        )

```

- Campos del modelo:
  - **title** es el título de la lesson.
  - **content** contenido de la asignatura que puede existir o no.
  - **subject** es una relacion 1:N con la asignatura de la lección.
- Métodos:
  - **str** Devuelve una representación legible del objeto.
  - **get_absolute_url** Devuelve la url absoluta del objeto en cuestión.

##### Enrrollment

```python
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='enrollments',
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        related_name='enrollments',
        on_delete=models.CASCADE,
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f'{self.student} {self.subject} enrolled at {self.enrolled_at} {self.mark}'
```

- Campos del modelo:
  - **student** relación 1:N entre el módelo user que identifica a un estudiante.
  - **subject** relación 1:N entre el módelo subject y la matrícula.
  - **enrolled_at** Fecha de la creación de la matrícula.
  - **mark** nota del estudiante obtenida en una asignatura. Utilización de validadores para restringir el valor de la nota entre 1 y 5.
- Métodos:
  - **str** Devuelve una representación legible del objeto.

## Urls

Dentro de las urls de subjects nos encontramos:

```python
app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('certificate/', views.request_certificate, name='certificate'),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/$',
        views.lesson_detail,
        name='lesson-detail',
    ),
    re_path('(?P<subject_code>[A-Z]{3})/lessons/add/', views.add_lesson, name='add-lesson'),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/edit/',
        views.edit_lesson,
        name='edit-lesson',
    ),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/delete/',
        views.delete_lesson,
        name='delete-lesson',
    ),
    re_path('(?P<subject_code>[A-Z]{3})/marks/edit/', views.edit_marks, name='edit-marks'),
    re_path('(?P<subject_code>[A-Z]{3})/marks/', views.mark_list, name='mark-list'),
    re_path('(?P<subject_code>[A-Z]{3})/', views.subject_detail, name='subject-detail'),
]
```

- **re_path** Expresión regular encargada de verificar la estructura semantica de la url proporcionada.

## Views

Dentro de las views de subjects nos encontramos con las siguientes vistas:

##### Subject list

Vista encargada de listar las asignaturas del usuario loggeado

```python
def is_all_marks_done(user):
    return user.enrollments.filter(mark__isnull=True).exists()

@login_required
def subject_list(request):
    user_enrollments = request.user.enrollments.exists()
    return render(
        request,
        'subjects/subject_list.html',
        dict(all_marks=is_all_marks_done(request.user), user_enrollments=user_enrollments),
    )
```

- `@login_required` decorador que asegura que solo los usuarios autenticados puedan acceder a esta vista.
- `user_enrollments` recuperamos las matrículas del usuario loggeado
- Retornamos la plantilla renderizada pasando como contexto dichas matrículas y las notas del usuario si estas ya se encuentran publicadas.
- `is_all_marks_done` funcion auxiliar que devuelve True si las notas ya estan publicadas

##### **Subject detail**

```python
@login_required
@auth_user_subject
def subject_detail(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    user_role = request.user.profile.get_role()
    match user_role:
        case 'Student':
            user_mark = Enrollment.objects.get(subject=subject, student=request.user).mark
        case 'Teacher':
            user_mark = None
    return render(
        request,
        'subjects/subject_detail.html',
        dict(lessons=lessons, subject=subject, mark=user_mark),
    )
```

- `@auth_user_subject` El usuario está registrado en este subject.
- `subject`: Obtenemos la asignatura perteneciente al código dado en la url.
- `lessons`: Obtenemos todas las lecciones de la asignatura obtenida.
- `user_role` esta variable se extrae el rol del usuario.
- Hacemos uso del match case para poder diferenciar entre un profesor y un alumno, pues el profesor no dispone de notas y el usuario si.

##### **Lesson detail**

```python
@login_required
@auth_user_subject
def lesson_detail(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    return render(request, 'subjects/lesson_detail.html', dict(lesson=lesson, subject=subject))

```

- `subject`: Obtenemos la asignatura con el código dado en la url.
- `lesson` : Obtenemos la lección con la pk dada en la url.

##### **Add lesson**

```python
@login_required
@validate_type_user
@auth_user_subject
def add_lesson(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            messages.success(request, 'Lesson was successfully added.')
            return redirect(subject)
    else:
        form = AddLessonForm()
    return render(request, 'subjects/add_lesson.html', dict(form=form))
```

- `@validate_type_user`:
- `subject`: Obtenemos la asignatura con el código dado en la url.
- Verificamos el método dado en request que sea POST. Despúes comenzamos a crear el formulario, validarlo y guardarlo en la base de datos.
- Si el método es incorrecto o sucede algún fallo devolvemos el formulario solo.

##### **Edit lesson**

```python

@login_required
@validate_type_user
@auth_user_subject
def edit_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            messages.success(request, 'Changes were successfully saved.')
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'subjects/edit_lesson.html', dict(lesson=lesson, form=form))
```

- `subject`: Obtenemos la asignatura con el código dado en la url.
- `lesson` : Obtenemos la lección con la pk dada en la url.
- Verificamos el método dado en request que sea POST. Despúes comenzamos a crear el formulario, validarlo y guardarlo en la base de datos.
- Si el método es incorrecto o sucede algún fallo devolvemos el formulario solo.

##### **Delete lesson**

```python
@login_required
@validate_type_user
@auth_user_subject
def delete_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    lesson.delete()
    messages.success(request, 'Lesson was successfully deleted.')
    return redirect('subjects:subject-detail', subject_code=subject.code)

```

- `subject`: Obtenemos la asignatura con el código dado en la url.
- `lesson` : Obtenemos la lección con la pk dada en la url.
- Extraemos ese lesson y lo eliminamos de la base de datos mediante el método por defecto de django para eliminar un objecto.

##### **Mark list**

```python
@login_required
@validate_type_user
@auth_user_subject
def mark_list(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    enrollments = Enrollment.objects.filter(subject=subject)
    return render(
        request, 'subjects/mark_list.html', dict(enrollments=enrollments, subject=subject)
    )
```

- `subject`: Obtenemos la asignatura con el código dado en la url.
- `enrollments` : Obtenemos la matrícula mediante la subject conseguida anteriormente.

##### **Edit marks**

```python
@login_required
@validate_type_user
@auth_user_subject
def edit_marks(request, subject_code):
    subject = Subject.objects.get(code=subject_code)

    """
    breadcrumbs = Breadcrumbs()
    breadcrumbs.add('My subjects', reverse('subjects:subject-list'))
    breadcrumbs.add(subject.code, reverse('subjects:subject-detail', args=[subject.code]))
    breadcrumbs.add('Marks', reverse('subjects:mark-list', args=[subject.code]))
    breadcrumbs.add('Edit marks')
    """
    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )

```

##### **Enroll subjects**

```python
@login_required
def enroll_subjects(request):
    message = 'Enroll in a subject'
    if request.method == 'POST':
        if (form := AddEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.add(subject)
            messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')
        else:
            return HttpResponseForbidden('Tienes que legir al menos una!')
    else:
        form = AddEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form, message=message))

```

##### **Uneroll Subjects**

```python

@login_required
def unenroll_subjects(request):
    message = 'Unenroll from a subject'
    if request.method == 'POST':
        if (form := UnEnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.remove(subject)
            messages.warning(request, 'Successfully unenrolled from the chosen subjects.')
            return redirect('subjects:subject-list')
        else:
            return HttpResponseForbidden('Tienes que elegir al menos una!')
    else:
        form = UnEnrollForm(request.user)
    return render(request, 'subjects/add_enroll.html', dict(form=form, message=message))
```

##### **Request certificate**

```python
@login_required
def request_certificate(request):
    role = request.user.profile.get_role()
    match role:
        case 'Student':
            if not request.user.enrollments.filter(mark__isnull=True).exists():
                base_url = request.build_absolute_uri('/')
                deliver_certificate.delay(base_url, request.user)
                return render(request, 'subjects/certificates/send.html')
            else:
                return HttpResponseForbidden('No te han puesto todas las notas')
        case 'Teacher':
            return HttpResponseForbidden('No tienes acceso a certificados')

```

- `role`: Conseguimos el rol del usuario logueado para hacer uso de dicho valor en el match case.
- En este miramos si es un estudiante o un profesor. Si es profesor, no tiene acceso al certificado. Si es estudiante, empezamos a construir el certificado mediantee `deliver_certificate.delay`.
