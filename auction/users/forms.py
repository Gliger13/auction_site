from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from users.models import User


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-form'

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        self.instance.password = make_password(self.cleaned_data['password'])
        return super().save(self)

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("Passwords not equals")
        return self.cleaned_data

    def clean_username(self):
        username = self.data['username']
        if not username:
            raise forms.ValidationError("Username contains forbidden characters")
        return username

    def get_user(self, request):
        user = authenticate(
            request,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return user


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-form'

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def get_user(self, request):
        return authenticate(
            request,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
