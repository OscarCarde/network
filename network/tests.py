from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
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