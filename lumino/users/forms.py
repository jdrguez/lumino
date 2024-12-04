from django import forms

from .models import Profile


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
