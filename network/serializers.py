from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    by = serializers.CharField(source='by.username', read_only=True)

    class Meta:
        model = Post
        fields = ['by', 'content', 'media', 'timestamp']