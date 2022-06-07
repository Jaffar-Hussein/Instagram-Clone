from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ImageForm, ProfileEditForm
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image, Profile


@login_required
def home(request):
    posts=Image.objects.all()
    return render(request, 'home.html',{"posts": posts})
@login_required
def explore(request):
    posts=Image.objects.all()
    return render(request, 'explore.html', {"posts": posts})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = form.save()
            profile = Profile(username=username, email=email)
            profile.save()
            messages.success(request, "Registration successful, Please Login")
            return redirect("login")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, template_name="auth/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'auth/login.html', context=context)


@login_required
def image_upload(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            caption = form.cleaned_data['caption']
            likes = 0
            profile = Profile.objects.all().filter(username=request.user.username).first()
            print(profile)
            form = Image(name=name, image=image, caption=caption,
                         likes=likes, profile=profile)
            form.save()
            print(form)

            messages.success(request, "Post created successful")
    form = ImageForm()

    context = {
        "form": form
    }

    return render(request, 'upload.html', context=context)


def logout_request(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    current_user = request.user
    user_profile = Profile.objects.all().filter(
        username=current_user.username).first()
    context = {
        "user_details": user_profile
    }
    return render(request, 'profile.html', context=context)


@login_required
def profile_edit(request):
    current_user = request.user
    user_profile = Profile.objects.all().filter(
        username=current_user.username).first()
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            print(2)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            profile = form.cleaned_data['profile']
            new_profile = user_profile(username=username, email=email, bio=bio, profile=profile)
            new_profile.save()
            print(new_profile.username)

    form = ProfileEditForm()
    
    context = {
        "user_details": user_profile,
        "form": form
    }

    return render(request, 'profile_edit.html',context=context)
