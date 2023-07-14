from rest_framework import serializers
from .models import Post, Profile

class PostSerializer(serializers.ModelSerializer):
    by = serializers.CharField(source='by.username', read_only=True)

    class Meta:
        model = Post
        fields = ['by', 'content', 'media', 'timestamp']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    ordered_posts = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializeMethodField()
    number_followed = serializers.SerializeMethodField()

    def get_ordered_posts(self, obj):
        instances = obj.odered_posts
        post_serializer = PostSerializer(instances, many=True)
        return post_serializer.data
    
    def get_number_of_followers(self, obj):
        return obj.number_of_followers

    def get_number_followed(self, obj):
        return obj.number_followed 

    class Meta:
        model: Profile
        fields = ['username', 'ordered_posts', 'number_of_followers', 'number_followed']