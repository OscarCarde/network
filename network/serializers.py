from rest_framework import serializers
from .models import Post, Profile

class PostSerializer(serializers.ModelSerializer):
    by = serializers.CharField(source='by.username', read_only=True)
    posted_since = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_posted_since(self, obj):
        return obj.posted_since
    
    def get_likes(self, obj):
        return obj.number_of_likes
    
    class Meta:
        model = Post
        fields = ['id', 'by', 'content', 'media', 'likes', 'posted_since']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    ordered_posts = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_followed = serializers.SerializerMethodField()

    def get_ordered_posts(self, obj):
        instances = obj.ordered_posts
        post_serializer = PostSerializer(instances, many=True)
        return post_serializer.data
    
    def get_number_of_followers(self, obj):
        return obj.number_of_followers

    def get_number_followed(self, obj):
        return obj.number_followed 

    class Meta:
        model =  Profile
        fields = ['username', 'about', 'profile_picture', 'number_of_followers', 'number_followed', 'ordered_posts' ]