from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import *
from .models import Post
from .serializers import PostSerializer

from .models import User

class Index(TemplateView):
    template_name = "network/index.html"
    extra_context = {"new_post_form": NewPostForm()}

    def post(self, request):
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.by = request.user
            new_post.save()
            
        else:
            return HttpResponseRedirect("/register/")
        
   

def posts(request):

    ''' posts API,
    get posts from database and load them in json
    '''
    #TODO:
    #get number of posts and start indice to get posts from
    number_of_posts = int(request.GET.get("num_posts") or 10)
    offset = int(request.GET.get("offset") or 0)

    #get posts from database from given index to 10th index
    posts = Post.objects.order_by("timestamp")[offset:offset+number_of_posts]
    #format the posts
    serializer = PostSerializer(posts, many=True)
    #return JSONResponse
    return JsonResponse({"posts": serializer.data})
    


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
