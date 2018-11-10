from django.db import models

# Create your models here.
class Profile(models.Model):
    """Class that extends the user profile from django"""
    user = models>ForeignKey(User,on_delete=models.CASCADE,default=1)
    profile_pic = models.ImageField(upload_to='profiles/')
    bio = models.CharField(max_length=250)

class Image(models.Model):
    """class defining the images"""
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=560)
    profile = models.ForeignKey(Profile,default=1)
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey(Comment,default=0)

class Comment(models.Model):
    """Class that defines the comments"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    image = models.ForeignKey(Image,on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=250)
    pub_time = models.DateTimeField(auto_now_add = True)
