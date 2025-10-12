from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings", views.listings, name = "listings"),
    path("new_listing/", views.new_listing, name = "new_listing"),
    path("edit_listing/<int:id>/", views.edit_listing, name = "edit_listing"), 
    path("watchlist_view", views.watchlist_view, name = "watchlist_view"),
    path("watchlist_add/<int:id>/", views.watchlist_add, name = "watchlist_add"),   
    ]
