from django import forms

from .models import Enrollment


class AddEnroll(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('title', 'content')
