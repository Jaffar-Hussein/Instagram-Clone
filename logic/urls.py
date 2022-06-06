from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path('upload', views.image_upload, name='upload'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('logout', views.logout_request, name='logout'),
    path('explore',views.explore, name='explore'),
]
