from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from users.models import User, Avatar


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input input-form'

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
            visible.field.widget.attrs['class'] = 'uk-input input-form'

    username_or_email = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def get_user(self, request):
        # Try authenticate by username
        user_by_username = authenticate(
            request,
            username=self.cleaned_data['username_or_email'],
            password=self.cleaned_data['password']
        )
        if user_by_username:
            return user_by_username
        else:
            # Try authenticate by email
            user = User.objects.get(email=self.cleaned_data['username_or_email'])
            if user:
                return authenticate(
                    request,
                    username=user.username,
                    password=self.cleaned_data['password']
                )


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.current_user = None
        self.is_new_email = None

        super(SettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input input-form'

    username = forms.CharField(
        label='Username:',
        max_length=15,
        widget=forms.TextInput,
        required=True,
    )
    first_name = forms.CharField(
        label='First name:',
        max_length=15,
        widget=forms.TextInput,
        required=False,
    )
    second_name = forms.CharField(
        label='Second name:',
        max_length=15,
        widget=forms.TextInput,
        required=False,
    )
    telephone = forms.CharField(
        label='Telephone:',
        max_length=11,
        widget=forms.TextInput,
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
        required=False,
    )
    image = forms.FileField(
        widget=forms.FileInput,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'second_name',
            'telephone',
            'email',
            'image',
        ]

    def save(self, commit=True):
        if self.cleaned_data.get('image'):
            avatar = Avatar.objects.filter(user=self.current_user)
            if avatar:
                avatar.delete()
            new_avatar = Avatar(user=self.current_user, image=self.image)
            new_avatar.save()
        if self.is_new_email:
            self.current_user.is_email_verified = False
            self.current_user.save()
        return super().save(self)

    def set_user(self, user):
        self.current_user = user

    def clean_username(self):
        username = self.data.get('username')
        if username == self.current_user.username:
            return username
        if not username or not username.isalnum():
            raise forms.ValidationError("Username contains forbidden characters")
        username_qs = User.objects.filter(username=username)
        if username_qs:
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.data.get('email')
        if email == self.current_user.email:
            return email
        if not email:
            raise forms.ValidationError("Email address contains forbidden characters")
        email_qs = User.objects.filter(email=email)
        if email_qs:
            raise forms.ValidationError("Email address already exists")
        self.is_new_email = True
        return email

    def clean_telephone(self):
        telephone = self.data.get('telephone')
        if not telephone:
            return None
        if telephone == self.current_user.telephone:
            return telephone
        if not telephone.isdigit():
            raise forms.ValidationError("Telephone contains forbidden characters")
        telephone_qs = User.objects.filter(telephone=telephone)
        if telephone_qs:
            raise forms.ValidationError("Telephone already exists")
        return telephone

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        if not first_name:
            return None
        if not first_name.isalpha():
            raise forms.ValidationError("First name contains forbidden characters")
        return first_name

    def clean_second_name(self):
        second_name = self.data.get('second_name')
        if not second_name:
            return None
        if not second_name.isalpha():
            raise forms.ValidationError("Second name contains forbidden characters")
        return second_name
