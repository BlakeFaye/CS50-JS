from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages 

from django.core.exceptions import ObjectDoesNotExist


from .models import User, Auction_Listing, User, Comment, Bid, Watchlist
from .forms import Auction_Listing_Form


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listings(request):
    return render(request, "auctions/listings.html", {
        "listings": Auction_Listing.objects.all()
    })

def new_listing(request):
    if request.method == 'POST':
        form = Auction_Listing_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = Auction_Listing_Form()
    return render(request, 'auctions/new_listing.html', {'form': form})

def edit_listing(request, auction_id):
    listing_instance = Auction_Listing.objects.get(pk=auction_id)
    print(f"listing_instance.id {listing_instance.id}")
    if request.method == 'GET':
        #On a besoin de repasser auction_id pour le réinjecter dans la watchlist
        context = {'form': Auction_Listing_Form(instance=listing_instance), 'id': id, 'auction_id':auction_id}
        return render(request,'auctions/edit_listing.html',context)
    elif request.method == 'POST':
        form = Auction_Listing_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
def watchlist(request):
    selected_watchlist = Watchlist.objects.all(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": Watchlist.objects.all()
    })

def addWatchlist(request, auction_id): 
    #TODO : Ajouter les contrôles  
    #Get watchlist of curent user
    auction_instance = Auction_Listing.objects.get(pk= auction_id)
    watch = Watchlist(user=request.user, auctions=auction_instance)  
    #To add the listing in the watchlist
    watch.save()
    return render(request, "auctions/listings.html", {
        "listings": Auction_Listing.objects.all()
    })

def removeWatchlist(request, auction_id):
    pass
    #TODO : afficher le remove si l'item est est déjà watchlisté
    #TODO : Ajouter le système de bid omg