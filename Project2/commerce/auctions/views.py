from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages 


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

def edit_listing(request, id):

    listing_instance = get_object_or_404(Auction_Listing, id=id)

    if request.method == 'GET':
        context = {'form': Auction_Listing_Form(instance=listing_instance), 'id': id}
        return render(request,'auctions/edit_listing.html',context)
    elif request.method == 'POST':
        form = Auction_Listing_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
def watchlist_view(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Auction_Listing.objects.all()
    })

def watchlist_add(request, id):
    listing_to_save = get_object_or_404(Auction_Listing, pk=id)
    # Check if the item already exists in that user watchlist
    print(Watchlist.objects)
    if Watchlist.objects.filter(user=request.user, item=id).exists():
        print("item already in watchlist")
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("auctions:index"))
    # Get the user watchlist or create it if it doesn't exists
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(listing_to_save)
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return render(request, "auctions/watchlist.html")