from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput())
    # required_css_class = 'required d-none'
    username.widget.attrs.update(
        {'class': 'form-control m-2 w-75 input-val', 'placeholder': 'Username'})
    password.widget.attrs.update(
        {'class': 'form-control m-2 w-75 input-val', 'placeholder': 'Password'})

    class Meta:
        model = Profile
        fields = ('username', 'password')
