import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like

def all_posts(request):
    return render(request, "network/all_posts.html")

def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def add_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_content = data.get("post_content", "")
    user = request.user

    post = Post(
        user=user,
        content = post_content
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)

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
    
def post(request, post_id):
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
def all_posts_data(request):
    posts = Post.objects
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def all_posts_likes(request):
    likes = Like.objects
    likes = likes.order_by("-id").all()
    return JsonResponse([like.serialize() for like in likes], safe=False)

def like_post(request, post_id):
    # Retrieve post data
    post = Post.objects.get(pk=post_id)
    user = request.user
    
    # Like/unlike logic
    try:
        #user already liked this post
        postLike = Like.objects.get(post=post, user=user)
        postLike.delete()

    except Like.DoesNotExist:
        #user hasn't liked this post
        postLike = Like(post=post, user=user)
        postLike.save()

    return JsonResponse({"message": "Post like switched successfully."}, 
                         status=201)


def get_post_likes(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    
    total_likes = Like.objects.filter(post = post_id).count()
    user_liked_post = False

    try:
        postLike = Like.objects.get(post=post, user=user)
        user_liked_post = True

    except Like.DoesNotExist:
        user_liked_post = False

    return JsonResponse({
        "post_id" : post_id,
        "total_likes" : total_likes,
        "user_liked_post": user_liked_post
    })

def edit_post(request, post_id):
    message = "POSTTTT"
    return JsonResponse({"message": message})

def get_user(request):
    pass
    # current_user = User.objects.get(username=request.user)
    # print(current_user)
    # return JsonResponse({
    #         "current_user" : current_user
    #     })

# https://stackoverflow.com/questions/46619473/django-how-do-you-get-field-from-another-model-in-a-view