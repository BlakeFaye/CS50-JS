
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts", views.all_posts, name="all_posts"),

    #Tools
    path("add_post", views.add_post, name="add_post"),
    path("like_post/<int:post_id>", views.like_post, name = "like_post"),
    path("edit_post", views.edit_post, name = "edit_post"),
    path("get_user", views.get_user, name = "get_user"),

    #API
    path("post/<int:post_id>", views.post, name = "post"),
    path("all_posts_data", views.all_posts_data, name="all_posts_data"),
    path("all_posts_likes", views.all_posts_likes, name="all_posts_likes"),
    path("get_post_likes/<int:post_id>", views.get_post_likes, name = "post"),
]
