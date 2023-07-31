from typing import Any, Dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import TemplateView
from .forms import *
from .models import Post
from .serializers import PostSerializer, ProfileSerializer
from django.core.paginator import Paginator

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
#TODO: refactor apis 

def get_allposts(request):
    ''' posts API,
    get posts from database and load them in json
    '''

    #get number of posts and start index to get posts from
    #number_of_posts = int(request.GET.get("num_posts") or 10)
    #offset = int(request.GET.get("offset") or 0)
    ''' change api call to /posts?page=${page_number}
    '''
    page_number = int(request.GET.get("page") or 1)

    #get posts from database
    posts = Post.objects.order_by("-timestamp")#[offset:offset+number_of_posts]
    # implement paginator
    pages = Paginator(posts, 10) 
    page = pages.page(page_number)
    #format the posts
    serializer = PostSerializer(page.object_list, many=True)

    for post in serializer.data:
        post_instance = Post.objects.get(id=post["id"])
        post["liked"] = request.user in post_instance.likes.all()
    #return JSONResponse
    return JsonResponse({"posts": serializer.data, "has_next": page.has_next(), "has_previous": page.has_previous()})

@login_required
def get_followed_posts(request):
    page_number = int(request.GET.get("page") or 1)
    posts = request.user.profile.followed_posts
    # implement paginator
    pages = Paginator(posts, 10) 
    page = pages.page(page_number)
    serializer = PostSerializer(page.object_list, many=True)
    for post in serializer.data:
        post_instance = Post.objects.get(id=post["id"])
        post["liked"] = request.user in post_instance.likes.all()
        #return JSONResponse
    return JsonResponse({"posts": serializer.data, "has_next": page.has_next(), "has_previous": page.has_previous()})

def get_profile_posts(request, user):
    page_number = int(request.GET.get("page") or 1)
    posts = Post.objects.filter(by=User.objects.get(username=user)).order_by("-timestamp")
    pages = Paginator(posts, 10)
    page = pages.page(page_number)
    post_serializer = PostSerializer(page.object_list, many=True)
    return JsonResponse({'posts': post_serializer.data, "has_next": page.has_next(), "has_previous": page.has_previous()})

    
def profile(request):
    ''' profile api,
    get information and posts about a user
    '''
    username = request.GET.get("username")
    profile = Profile.objects.get(user = User.objects.get(username=username))
    profile_serializer = ProfileSerializer(profile)

    json_response = {'profile': profile_serializer.data}

    is_followed = profile.user in request.user.profile.following.all()
    json_response["profile"]["is_following"] = is_followed

    return JsonResponse(json_response)

@login_required
def like(request, id):
    post = Post.objects.get(id=id)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    return JsonResponse(dict())


@login_required
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
    
@login_required
def edit_post(request, id):

    message = "couldn't edit the post"

    #process the json data
    raw_content = request.body
    loaded_content = json.loads(raw_content)
    content = loaded_content.get("new_content")

    post = Post.objects.get(id=id)
    if post.by == request.user:
        post.content = content
        post.save()
        message = "post edited successfully"
    else:
        message = "post doesn't belong to logged-in user"

    return JsonResponse({"edited": message})
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
