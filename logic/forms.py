from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Image, Comments


class NewUserForm(UserCreationForm):
    email = forms.EmailField(
	    required=True, widget=forms.EmailInput(attrs={'class': 'my-3 input-val'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['class'] = 'my-3 input-val'
        self.fields['username'].widget.attrs['class'] = 'input-val'
        self.fields['password1'].widget.attrs['class'] = 'input-val'

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


class ImageForm(forms.ModelForm):
    name = forms.CharField(max_length=40)
    image = forms.ImageField()
    caption = forms.CharField(max_length=80)

    class Meta:
        model = Image
        fields = ('name', 'image', 'caption')
    name.widget.attrs.update(
        {'class': 'form-control m-2 w-100 input-val', 'placeholder': 'Enter Image name'})
    caption.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Enter the caption'})
    image.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Enter Image'})
        
class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    bio = forms.CharField(max_length=50,widget=forms.Textarea)
    profilephoto = forms.ImageField()
    
    class Meta:
        model = Profile
        fields = ('username', 'profilephoto', 'bio','email')
    username.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Username'})
    email.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Email'})
    profilephoto.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Profile Photo'})
    bio.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Enter bio','rows':4, 'cols':40})
    
class CommentsForm(forms.ModelForm):
    comments=forms.CharField(max_length=50)

    class Meta:
        model=Comments
        fields=('comments',)
    
    comments.widget.attrs.update(
        {'class': 'form-control m-2  input-val', 'placeholder': 'Type comment here ...'})

    