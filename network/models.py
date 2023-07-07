from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length = 1000)
    media = models.ImageField(upload_to='media/post_media', blank=True)

    by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.by.username} said: {self.content[:9]}... on {self.timestamp.strftime('%d-%m-%Y')} at {self.timestamp.strftime('%H:%M')}"