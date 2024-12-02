from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth import get_user_model


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
            Submit('login', 'Login', css_class='w-100 mt-2 mb-2'),
        )


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

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        return user
