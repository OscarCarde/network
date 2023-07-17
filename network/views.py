from typing import Any, Dict
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import *
from .models import Post
from .serializers import PostSerializer, ProfileSerializer

from .models import User

class Index(TemplateView):
    template_name = "network/index.html"
    extra_context = {"new_post_form": NewPostForm()}


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        #add the profile of the logged-in user to the context
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context["profile"] = profile
        return context

    def post(self, request):
        new_post_form = NewPostForm(request.POST, request.FILES)
        if new_post_form.is_valid():
            new_post = new_post_form.save(commit=False)
            new_post.by = request.user
            new_post.save()
            return HttpResponseRedirect("/")
            
        else:
            return HttpResponseRedirect("/register/")
        
        
   
#____________APIs_________________________

def get_posts(request):
    ''' posts API,
    get posts from database and load them in json
    '''

    #get number of posts and start index to get posts from
    number_of_posts = int(request.GET.get("num_posts") or 10)
    offset = int(request.GET.get("offset") or 0)
    
    #get posts from database from given index to 10th index
    posts = Post.objects.order_by("-timestamp")[offset:offset+number_of_posts]
    #format the posts
    serializer = PostSerializer(posts, many=True)
    #return JSONResponse
    return JsonResponse({"posts": serializer.data})
    
def profile(request):
    ''' profile api,
    get information and posts about a user
    '''
    username = request.GET.get("username")

    profile = Profile.objects.get(user = User.objects.get(username=username))

    serializer = ProfileSerializer(profile)

    json_response = {'profile': serializer.data}

    is_followed = profile.user in request.user.profile.following.all()
    json_response["profile"]["is_following"] = is_followed

    return JsonResponse(json_response)

def like(request, id):
    post = Post.objects.get(id=id)
    post.likes.add(request.user)
    return JsonResponse(dict())



def follow(request, username):
    profile = Profile.objects.get(user=request.user)
    user_to_follow = User.objects.get(username=username)

    if user_to_follow:
        if user_to_follow in profile.following.all():
            profile.following.remove(user_to_follow)
            return JsonResponse({"followed":False})
        else:
            profile.following.add(user_to_follow)
            return JsonResponse({"followed": True})
    else:
        return JsonResponse({"followed": None})
#_________________________________________________________

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #create the corresponding profile
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
