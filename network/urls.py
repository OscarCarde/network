
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.get_posts, name="posts"),
    path("profile", views.profile, name="profile"),
    path("like", views.like, name="like"),
    path("follow/<str:username>", views.follow, name="follow")
]
