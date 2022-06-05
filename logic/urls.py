from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path("register", views.register_request, name="register")
]