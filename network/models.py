from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField(User, blank=True, related_name="followers")
    profile_picture = models.ImageField(upload_to='media/profile_pictures', blank=True)
    about = models.CharField(max_length=1000, blank=True)

    @property
    def number_of_followers(self):
        return self.user.followers.count()
    @property
    def number_followed(self):
        return self.following.count()
    
    @property
    def ordered_posts(self):
        return self.user.posts.order_by("-timestamp")
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Post(models.Model):
    content = models.CharField(max_length = 10000)
    media = models.ImageField(upload_to='media/post_media', blank=True)

    by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("User", blank=True, related_name = "liked")

    @property
    def number_of_likes(self):
        return self.likes.count()
    
    @property
    def posted_since(self):
        return timesince(self.timestamp, timezone.now()) + " ago"

    def __str__(self):
        return f"{self.by.username} said: {self.content[:9]}... on {self.timestamp.strftime('%d-%m-%Y')} at {self.timestamp.strftime('%H:%M')}"