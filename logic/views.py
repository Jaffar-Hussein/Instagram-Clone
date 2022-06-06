from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ImageForm
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
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

            messages.success(request, "Successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'auth/login.html', context=context)


def image_upload(request):
    context = {
        "form": form
    }
    form = ImageForm()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            caption = form.cleaned_data['caption']
            form = ImageForm(name=name, image=image, caption=caption)
            form.save()
            print(form)

            messages.success(request, "Post created successful")

    return render(request, 'home.html', context=context)
