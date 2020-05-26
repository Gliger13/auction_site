from django import forms

from users.models import User


class RegistrationForm(forms.ModelForm):
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

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("Passwords not equals")
        return self.cleaned_data

    def clean_username(self):
        username = self.data['username']
        if not username.isalpha():
            raise forms.ValidationError("Username contains forbidden characters")
        return username

