from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class SignupUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Opcional')

    class Meta:
        model = Usuario
        fields = ['usuario', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
