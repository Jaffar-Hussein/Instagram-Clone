from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ImageForm, ProfileEditForm
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image, Profile
from django.contrib.auth.models import User


@login_required
def home(request):
    posts = Image.objects.all()
    return render(request, 'home.html', {"posts": posts})


@login_required
def explore(request):
    posts = Image.objects.all()
    return render(request, 'explore.html', {"posts": posts})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
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
            profile = Profile.objects.all().filter(username=request.user.username).first()
            profile.save()
            print(profile)
            form = Image(name=name, image=image, caption=caption,
                         profile=profile)
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
    # user_profile = Profile.objects.all().filter(
    #     username=current_user.username).first()
    print(current_user)
    print(current_user.profile)
    context = {
        "user_details": current_user.profile
    }
    return render(request, 'profile.html', context=context)


@login_required
def profile_edit(request):
    # current_user = request.user
    # user_profile = Profile.objects.all().filter(
    #     user=current_user)
      
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = User.objects.filter(username=request.user.username)
            user_profile =Profile.objects.all().filter(username = current_user.first().username)
            # Students.objects.select_for_update().filter(id=3).update(score = 10)
            print(user_profile)
            print(current_user[0].username)
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            profilephoto = form.cleaned_data['profilephoto']
            print (username)
            user_profile.update(username = username)
            auth_cred =  request.user
            auth_cred.username = username
            auth_cred.save()
            print(request.user.username)
            user_profile.email = email 
            user_profile.bio = bio
            user_profile.profilephoto = profilephoto
            
          
            print(
                user_profile
            )
            return redirect('profile')
            
    current_user = request.user
    user_profile = Profile.objects.all().filter(
        user=current_user).first()
    form = ProfileEditForm()

    context = {
        "user_details": user_profile,
        "form": form
    }

    return render(request, 'profile_edit.html', context=context)
