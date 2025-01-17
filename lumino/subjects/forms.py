from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Row, Submit
from django import forms

from .models import Enrollment, Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        

class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddEnrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.enrolled_subjects.all()
        )
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'),
            Submit('enroll', 'Enroll'),
        )


class UnEnrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = user.enrolled_subjects.all()

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'),
            Submit('unenroll', 'Unenroll'),
        )


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']


class EditMarkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-2">{% student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))
