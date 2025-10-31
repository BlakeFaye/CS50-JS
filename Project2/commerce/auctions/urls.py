from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings", views.listings, name = "listings"),
    path("new_listing/", views.new_listing, name = "new_listing"),
    path("edit_listing/<int:auction_id>/", views.edit_listing, name = "edit_listing"),
    path("listing/<int:auction_id>/", views.listing, name = "listing"), 
    path("watchlist", views.watchlist, name = "watchlist"),
    path("edit_listing/<int:auction_id>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("edit_listing/<int:auction_id>/removeWatchlist", views.removeWatchlist, name="removeWatchlist")
    ]
