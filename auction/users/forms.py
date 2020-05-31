from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from users.models import User


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-form'

    username = forms.CharField(
        max_length=15
    )
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
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords not equals")
        return self.cleaned_data

    def clean_username(self):
        username = self.data.get('username')
        if not username:
            raise forms.ValidationError("Username contains forbidden characters")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.data.get('email')
        if not email:
            raise forms.ValidationError("Email contains forbidden characters")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email already exists")
        return email

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
