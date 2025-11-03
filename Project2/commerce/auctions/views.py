from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.core.exceptions import ValidationError

from .models import User, Auction_Listing, User, Comment, Bid, Watchlist
from .forms import Auction_Listing_Form, Bid_Form, Auction_Listing_Form_RO


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
    current_user = request.user

    return render(request, "auctions/listings.html", {
        "listings": Auction_Listing.objects.all(),
        'current_user':current_user
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


def listing(request, auction_id):
    listing_instance = Auction_Listing.objects.get(pk=auction_id)

    bids = Bid.objects.filter(listing=listing_instance)
    max_bid = list(bids.aggregate(Max("amount", default=0)).values())[0]
    user_max_bid = list(bids.filter(user=request.user).aggregate(Max("amount", default=0)).values())[0]
    
    is_watchlisted = False
    try:
        Watchlist.objects.get(user=request.user, auctions=listing_instance)
        is_watchlisted = True
    except:
        print("item not watchlisted")
        pass

    if request.method == 'GET':
        context = {
                'listing_form': Auction_Listing_Form_RO(instance=listing_instance), 
                'bid_form': Bid_Form(),
                'id': id, 'auction_id':auction_id,
                'is_watchlisted':is_watchlisted,
                'max_bid' : max_bid, 'user_max_bid':user_max_bid}
        return render(request,'auctions/listing.html', context)
    
    elif request.method == 'POST':
        listing_price = listing_instance.price
        bid_form = Bid_Form(request.POST, max_bid, listing_price)
        if bid_form.is_valid():
            user_bid = bid_form.save(commit=False)
            user_bid.user = request.user
            user_bid.listing = listing_instance
            user_bid.save()
            return redirect('listing', auction_id=auction_id)

        #Si un des formulaires n'est pas valide alors on retourne la page à nouveau ce qui permet de display les erreurs
        context = {
            'listing_form': Auction_Listing_Form_RO(instance=listing_instance), 
            'bid_form': bid_form,
            'id': id, 'auction_id':auction_id,
            'max_bid' : max_bid, 'user_max_bid':user_max_bid}
        return render(request,'auctions/listing.html', context)


def edit_listing(request, auction_id):
    listing_instance = Auction_Listing.objects.get(pk=auction_id)

    #partie pour récupérer les max bid général et par user
    bids = Bid.objects.filter(listing=listing_instance)
    max_bid = list(bids.aggregate(Max("amount", default=0)).values())[0]
    
    #récup du formulaire
    if request.method == 'GET':               
        #partie pour voir si le listing est watchlisté
        is_watchlisted = False
        try:
            Watchlist.objects.get(user=request.user, auctions=listing_instance)
            is_watchlisted = True
        except:
            print("item not watchlisted")
            pass
        
        context = {
            'listing_form': Auction_Listing_Form(instance=listing_instance), 
            'bid_form': Bid_Form(),
            'id': id, 'auction_id':auction_id,
            'is_watchlisted':is_watchlisted,
            'max_bid' : max_bid}
        return render(request,'auctions/edit_listing.html', context)
    
    elif request.method == 'POST':
        listing_form = Auction_Listing_Form(request.POST, instance=listing_instance)
        if listing_form.is_valid():
            listing_form.save()
            return redirect('edit_listing', auction_id=auction_id)

        #Si un des formulaires n'est pas valide alors on retourne la page à nouveau ce qui permet de display les erreurs
        context = {
            'listing_form': Auction_Listing_Form(instance=listing_instance), 
            'id': id, 'auction_id':auction_id,
            'max_bid' : max_bid}
        return render(request,'auctions/edit_listing.html', context)   
        
#TODO : 4 versions de formulaires : 
    # - Si auteur et open : Edition et pas de bid
    # - Si auteur et fermé : Lecture seule, bouton rouvrir, pas de bid
    # - Si consulte et open : Lecture seule, bid
    # - Si consulte et fermé : Lecture seule, pas de bid

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": Watchlist.objects.all()
    })


def addWatchlist(request, auction_id): 
    auction_instance = Auction_Listing.objects.get(pk= auction_id)
    watch = Watchlist(user=request.user, auctions=auction_instance)  
    #To add the listing in the watchlist
    watch.save()
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": Watchlist.objects.all()
    })


def removeWatchlist(request, auction_id):
    auction_instance = Auction_Listing.objects.get(pk= auction_id)
    watch = Watchlist.objects.get(user=request.user, auctions=auction_instance) 
    watch.delete()
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": Watchlist.objects.all()
    })
