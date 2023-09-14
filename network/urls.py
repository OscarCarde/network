
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #######__apis__########
    path("posts", views.get_allposts, name="posts"),
    path("posts/<str:user>", views.get_profile_posts, name="profile_posts"),
    path("following", views.get_followed_posts, name="following"),
    path("profile", views.get_profile, name="profile"),
    path("like/<int:id>", views.like, name="like"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit_post, name="edit")
]
