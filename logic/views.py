from cmath import log
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ImageForm, ProfileEditForm,CommentsForm
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image, Profile, Followers, Like, Comments
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@login_required
def home(request):
    posts = Image.objects.all()
    user_display = request.user
    users = User.objects.all()
    users = User.objects.all().exclude(id=request.user.id)
    followers_posts = Image.objects.all()
    followed = [i for i in User.objects.all() if Followers.objects.filter(
        followers=request.user, followed=i)]
    if followed:
        for i in followed:

            followers_posts = Image.objects.all().filter(user=i).order_by('pub_date')

            followers_posts = Image.objects.all()
    else:
        followers_posts = Image.objects.all().filter(
            user=request.user).order_by('pub_date')

    return render(request, 'home.html', {"posts": posts, "user_display": user_display, "users": users, "followed": followed, "followers_posts": followers_posts},)


@login_required
def explore(request):
    posts = Image.objects.all()
    user_display = request.user
    return render(request, 'explore.html', {"posts": posts, "user_display": user_display})


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
    followed = [i for i in User.objects.all() if Followers.objects.filter(
    followers=request.user, followed=i)]

    followers = [i for i in User.objects.all() if Followers.objects.filter(
    followers=i, followed=request.user)]

    followed_number = len(followed)
    followers_number = len(followers)
    print(followers)
    context = {
        "user_details": current_user.profile,
        "posts": posts,
        "number": number,
        "followed_number": followed_number,
        "followers_number": followers_number,
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
        "user_display": user_display,
        'number': len(Image.objects.all().filter(user=request.user.id))
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


@csrf_exempt
@login_required
def likes(request, post_id):
    current_user = request.user
    current_user_like = Like.objects.all().filter(
        lovers_id=current_user.id, post_id=post_id)
    if current_user_like.first():
        current_user_like.delete()

    else:
        new = Like(lovers_id=current_user.id, post_id=post_id)
        new.save()
    number = str(Like.objects.filter(post_id=post_id).count())

    return HttpResponse(number)


@login_required
def search_results(request):
    image = User.objects.all()

    if 'username' in request.GET and request.GET['username']:
        searched_term = request.GET['username']
        searched_user = Profile.search_user(searched_term)
        followed = [i for i in User.objects.all() if Followers.objects.filter(
        followers=request.user, followed=i)]
        message = f"{searched_term}"
        image = Profile.objects.all()
        return render(request, 'search_results.html', {"message": message, 'searched_user': searched_user, 'followed':followed})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search_results.html', {"message": message, "image": image})


@login_required
def comments(request, post_id):
    posts = Image.objects.filter(id=post_id).first()
    print(posts)
    all_comments = Comments.objects.all().filter(image_comment=posts)
   
    if request.method == "POST":
        form = CommentsForm(request.POST,request.FILES)

        if form.is_valid():
            comment = form.cleaned_data['comments']
            form=Comments(comments=comment,image_comment=posts,user=request.user)
            form.save()
    form = CommentsForm()

    context ={
        "posts": posts,
        "form": form,
        "all_comments": all_comments
    }
    return render(request, 'comments.html',context=context)

@login_required
def image_detail(request, id):
    posts = Image.objects.filter(id=id).first()

    context ={
        "posts": posts,
        
    }
    return render(request, 'detail.html',context=context)