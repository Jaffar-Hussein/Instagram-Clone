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
    user_display = request.user
    users = User.objects.all()
    username = request.user.username
    users = User.objects.all().exclude(id=request.user.id)
    followers_posts=Image.objects.all()

    followed = [i for i in User.objects.all() if Followers.objects.filter(
        followers=request.user, followed=i)]
    if followed:
        for i in followed:
            
                print(i)
                followers_posts=Image.objects.all().filter(user=i).order_by('pub_date')
                print(followers_posts)
            
                followers_posts=Image.objects.all()
    else:
        followers_posts=Image.objects.all().filter(user=request.user).order_by('pub_date')

        
    
    return render(request, 'home.html', {"posts": posts, "user_display": user_display, "users": users, "followed": followed,"followers_posts":followers_posts},)


@login_required
def explore(request):
    posts = Image.objects.all()
    user_display = request.user
    return render(request, 'explore.html', {"posts": posts,"user_display": user_display})


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
    user_display = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            caption = form.cleaned_data['caption']
            
            form = Image(name=name, image=image, caption=caption,
                         user=request.user)
            form.save()
            messages.success(request, "Post created successful")
            return redirect('home')
    form = ImageForm()

    context = {
        "form": form,
        "user_display": user_display
    }
    return render(request, 'upload.html', context=context)


def logout_request(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user_display = request.user
    
    current_user = request.user
    posts = Image.objects.all().filter(user=request.user.id)
    number = len(posts)
    context = {
        "user_details": current_user.profile,
        "posts": posts,
        "number": number,
        "user_display": user_display
    }
    return render(request, 'profile.html', context=context)


@login_required
def profile_edit(request):
    user_display = request.user
    
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
        "form": form,
        "user_display": user_display
    }
    return render(request, 'profile_edit.html', context=context)


@login_required
def followers(request, user_id):
    current_user = request.user
    other_user = User.objects.get(id=user_id)
    followers = Followers.objects.filter(
        followers=current_user, followed=other_user)

    if followers:
        followers.delete()
    else:
        new_follower = Followers(followers=current_user, followed=other_user)
        new_follower.save()
    return redirect("home")
