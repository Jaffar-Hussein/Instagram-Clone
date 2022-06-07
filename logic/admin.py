from django.contrib import admin
from .models import Image, Profile,Followers
# Register your models here.



admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Followers)
