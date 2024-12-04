from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')


class AddEnroll(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.students_subjects.all
        )
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('subject'),
            Submit('enroll', 'Enroll'),
        )
