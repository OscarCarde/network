from django.test import Client, TestCase
from .models import *
from datetime import datetime, timedelta
from .serializers import *
import json
from collections import OrderedDict

# Create your tests here.

class ProfileTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="Alex", email="alex@gmail.com", password="1234")
        user2 = User.objects.create_user(username="Boris", email="boris@gmail.com", password="1234")
        user3 = User.objects.create_user(username="Callum", email="callum@gmail.com", password="1234")

        Profile.objects.create(user=user1, about="Hi I'm Alex and I love Aerobics")
        Profile.objects.create(user=user2, about="Be warned, I am Boris")
        Profile.objects.create(user=user3, about="Certain people really like cheese")

        Post.objects.create(id=1111, content="I'm eating maccaroni", by=user3)
        Post.objects.create(id=2222, content="Today is Tuesday", by=user1, timestamp=datetime(year=2023, month=8, day=1)+ timedelta(hours=1))
        Post.objects.create(id=3333, content="Today is Monday", by=user1, timestamp=datetime(year=2023, month=7, day=31, ))
        Post.objects.create(id=4444, content="Today is Monday", by=user1, timestamp=datetime(year=2022, month=7, day=1))
        

    def test_number_of_followers(self):
        alex_pr = User.objects.get(username="Alex").profile
        boris = User.objects.get(username="Boris")
        boris_pr = boris.profile
        alex_pr.following.add(boris)
        self.assertEquals(boris_pr.number_of_followers, 1, "something went wrong in the number_of_followers custom property in the Profile model")
        self.assertEqual(alex_pr.number_of_followers, 0, "something went wrong in the number_of_followers custom property in the Profile model")
        alex_pr.following.remove(boris)

    def test_number_followed(self):
        alex = User.objects.get(username="Alex")
        boris = User.objects.get(username="Boris")
        callum = User.objects.get(username="Callum")

        alex.profile.following.add(boris)
        alex.profile.following.add(callum)

        self.assertEqual(alex.profile.number_followed, 2, "something went wrong in the numberfollowed custom property in the Profile model")
        self.assertEqual(boris.profile.number_followed, 0, "something went wrong in the numberfollowed custom property in the Profile model")
        alex.profile.following.remove(boris)
        alex.profile.following.remove(callum)

    '''def test_ordered_posts(self):
        alex = User.objects.get(username="Alex")
        post1 = Post.objects.get(id=2222)
        post2 = Post.objects.get(id=3333)
        post3 = Post.objects.get(id=4444)
        self.assertListEqual(list(alex.profile.ordered_posts), [post1, post2, post3], "something went wrong with the ordered_posts property of the Profile model")

    def test_followed_posts(self):

        boris = User.objects.get(username="Boris").profile
        alex = User.objects.get(username="Alex")
        callum = User.objects.get(username="Callum")


        post1 = Post.objects.get(id=1111)
        post2 = Post.objects.get(id=2222)
        post3 = Post.objects.get(id=3333)
        post4 = Post.objects.get(id=4444)

        boris.following.add(alex)
        boris.following.add(callum)

        self.assertListEqual(list(boris.followed_posts.values_list('id', flat=True)), [post1.id, post2.id, post3.id, post4.id], "something went wrong with the followed_posts property of the Profile model")'''
    
class ApiTestCase(TestCase):

    def setUp(self):

        user1 = User.objects.create_user(username="Alex", email="alex@gmail.com", password="1234")
        user2 = User.objects.create_user(username="Boris", email="boris@gmail.com", password="1234")
        user3 = User.objects.create_user(username="Callum", email="callum@gmail.com", password="1234")

        Profile.objects.create(user=user1, about="Hi I'm Alex and I love Aerobics")
        Profile.objects.create(user=user2, about="Be warned, I am Boris")
        Profile.objects.create(user=user3, about="Certain people really like cheese")

        Post.objects.create(id=1111, content="I'm eating maccaroni", by=user3)
        Post.objects.create(id=2222, content="Today is Tuesday", by=user1, timestamp=datetime(year=2023, month=8, day=1)+ timedelta(hours=1))
        Post.objects.create(id=3333, content="Today is Monday", by=user1, timestamp=datetime(year=2023, month=7, day=31, ))
        Post.objects.create(id=4444, content="Today is Monday", by=user1, timestamp=datetime(year=2022, month=7, day=1))

        
    def test_get_allposts(self):
        #client
        c = Client()
        c.post("/login/", {"username": "Alex", "password": "1234"})

        #get posts
        response = c.get("/posts?page=1")
        api_posts = response.json()["posts"]
        
        #store posts in a list of ordered dictionaries 
        posts = []
        for post in api_posts:
            #remove liked field to compare posts 
            post.pop('liked')
            posts.append(OrderedDict(post.items()))
        
        #get serialized posts
        json_posts = PostSerializer(Post.objects.order_by("-timestamp"), many = True)

        self.assertListEqual(json_posts.data, posts, f"something went wrong when retreiving all posts\n Expected {list(json_posts.data)}")
        c.logout()

    def test_get_followed_posts(self):
        #client
        c = Client()
        c.post("/login/", {"username": "Alex", "password": "1234"})
        
        #get posts
        try:
            response = c.get("/following?page=1")
            api_posts = response.json()["posts"]
        except ValueError:
            pass
        else:
            #store posts in a list of ordered dictionaries 
            posts = []
            for post in api_posts:
                #remove liked field to compare posts 
                post.pop('liked')
                posts.append(OrderedDict(post.items()))

            #retreive followed posts
            followed_posts = Profile.objects.get(user=User.objects.get(username="Alex")).followed_posts
            followed_posts_serialized = PostSerializer(followed_posts, many=True)
            followed_posts_data  = followed_posts_serialized.data

            self.assertListEqual(followed_posts_data, posts, "something went wrong when retreiving followed posts ")

    def test_get_profile_posts(self):
        #client
        c = Client()
        c.post("/login/", {"username": "Alex", "password": "1234"})
        self.assertListEqual([0], [1], "something went wrong when retreiving profile posts ")

    def test_get_profile(self):
        #client
        c = Client()
        c.post("/login/", {"username": "Alex", "password": "1234"})
        self.assertEqual(0, 1, "something went wrong when retreiving profile details ")

    def test_edit_post(self):
        #client
        c = Client()
        c.post("/login/", {"username": "Alex", "password": "1234"})
        self.assertEqual(0, 1, "something went wrong when updating post")
