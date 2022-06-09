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
    
    @classmethod
    def search_user(cls,name):
        """
        search for an image by category
        """
        img = cls.objects.filter(user__username__icontains=name)
        return img



class Image(models.Model):
    name = models.CharField(max_length=40, null=False)
    image = CloudinaryField("image")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Images")
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
    
    @classmethod
    def search_images(cls, caption):
        """
        search for an image by category
        """
        img = cls.objects.filter(caption__icontains=caption)
        return img

class Followers(models.Model):
    followers = models.ForeignKey(User, related_name='followers',on_delete=models.CASCADE)
    followed=models.ForeignKey(User,related_name='followed',on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(Image, related_name='likes',on_delete=models.CASCADE)
    lovers = models.ForeignKey(User, related_name='posts_liked',on_delete=models.CASCADE)

class Comments(models.Model):
    comments = models.CharField(max_length=50, null=False)
    image_comment = models.ForeignKey(Image, related_name='comment_image',on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='posts_comments',on_delete=models.CASCADE)
