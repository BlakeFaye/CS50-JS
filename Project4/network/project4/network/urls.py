
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

    #API
    path("post/<int:post_id>", views.post, name = "post"),
    path("all_posts_data", views.all_posts_data, name="all_posts_data"),
    path("all_posts_likes", views.all_posts_likes, name="all_posts_likes"),
    path("total_likes/<int:post_id>", views.total_likes, name = "post"),
]
