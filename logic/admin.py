from django.contrib import admin
from .models import Image, Profile
# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display=("username","email","bio")
    list_filter=("username","email")


admin.site.register(Profile, AlbumAdmin)
admin.site.register(Image)
