from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField()
    profilephoto = CloudinaryField("profilephoto")
    bio = models.TextField()

    def __str__(self):
        return self.username

    @classmethod
    def save_profile(cls, profile):
        cls.save(profile)

    @classmethod
    def update_profile(cls, profile):
        cls.update(profile=profile)

    @classmethod
    def delete_profile(cls, profile):
        cls.delete(profile)


class Image(models.Model):
    name = models.CharField(max_length=40, null=False)
    image = CloudinaryField("image")
    profile = models.ForeignKey(Profile)
    likes = models.IntegerField()
    comments = models.TextField()
    caption = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.name

    @classmethod
    def save_image(cls, image):
        cls.save()

    @classmethod
    def delete_image(cls, image_id):
        cls.delete(id=image_id)

    @classmethod
    def update_caption(cls, caption):
        cls.update(caption=caption)
