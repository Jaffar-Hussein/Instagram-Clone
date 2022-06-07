from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    profilephoto = CloudinaryField("profilephoto")
    bio = models.TextField()
    user=models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Profile: {self.username} : email: {self.email} : profile: {self.profilephoto} : category: {self.bio}"


    def __str__(self):
        return self.user.username

    @classmethod
    def save_profile(cls, profile):
        cls.save(profile)

    @classmethod
    def update_profile(cls, username,email,bio,profilephoto):
        cls.update(username=username, email=email, bio=bio, profilephoto=profilephoto)

    @classmethod
    def delete_profile(cls, profile):
        cls.delete(profile)


class Image(models.Model):
    name = models.CharField(max_length=40, null=False)
    image = CloudinaryField("image")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
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

class Followers(models.Model):
    followers = models.ForeignKey(User, related_name='followers',on_delete=models.CASCADE, default=0)
    followed=models.ForeignKey(User,related_name='followed',on_delete=models.CASCADE,default=0)


class Like(models.Model):
    post = models.ForeignKey(Image, related_name='followers',on_delete=models.CASCADE,default=0)


