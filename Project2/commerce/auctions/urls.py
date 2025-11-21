from django.urls import path

from . import views

urlpatterns = [
    path("", views.listings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings", views.listings, name = "listings"),
    path("categories", views.categories, name = "categories"),
    path("category/<str:cat_name>", views.category, name = "category"),
    path("new_listing/", views.new_listing, name = "new_listing"),
    path("listing/<int:auction_id>/", views.listing, name = "listing"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("listing/<int:auction_id>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("listing/<int:auction_id>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("listing/<int:auction_id>/closeAuction", views.closeAuction, name="closeAuction"),
    ]
