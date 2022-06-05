from django.shortcuts import render, redirect
from .forms import NewUserForm,LoginForm
# Create your views here.
from django.contrib.auth import login,authenticate
from django.contrib import messages


def home(request):
    return render(request, 'layout.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, template_name="auth/register.html", context={"register_form": form})


def login_request(request):
	form = LoginForm()
	context = {
		"form": form,
	}
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			
			messages.success(request, "Successfully logged in")
			return redirect ('home')
		else:
			messages.error(request, "Invalid username or password")
			return redirect ('login')
		
	context = {
		"form": form,
	}
	return render(request, 'auth/login.html', context=context)
