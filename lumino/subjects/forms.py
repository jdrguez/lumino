from django import forms
from .models import Lesson

class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title','content')

class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')