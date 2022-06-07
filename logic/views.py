from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ImageForm, ProfileEditForm
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image, Profile, Followers
from django.contrib.auth.models import User


@login_required
def home(request):
    posts = Image.objects.all()
    username = request.user.username
    users = User.objects.all()
    followed = [i for i in User.objects.all() if Followers.objects.filter(
        followers=request.user, followed=i)]
    print(followed)
    
    return render(request, 'home.html', {"posts": posts, "username": username, "users": users, "followed": followed},)


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
            profile = Profile.objects.all().filter(id=request.user.id).first()
            profile.save()
            print(profile)
            form = Image(name=name, image=image, caption=caption,
                         profile=profile)
            form.save()
            messages.success(request, "Post created successful")
            return redirect('home')
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
    posts = Image.objects.all().filter(profile__id=request.user.id)
    number = len(posts)
    context = {
        "user_details": current_user.profile,
        "posts": posts,
        "number": number
    }
    return render(request, 'profile.html', context=context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            profilephoto = form.cleaned_data['profilephoto']
            profile = Profile.objects.get(id=request.user.id)
            profile.profilephoto = profilephoto
            profile.bio = bio
            profile.save()
            User.objects.filter(id=request.user.id).update(
                email=email, username=username)
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


@login_required
def followers(request, user_id):
    current_user = request.user.id
    current_user = User.objects.get(id=current_user)
    other_user = User.objects.get(id=user_id)
    followers = Followers.objects.filter(
        followers=current_user, followed=other_user)

    if followers:
        followers.delete()
    else:
        new_follower = Followers(followers=current_user, followed=other_user)
        new_follower.save()
    return redirect("home")
