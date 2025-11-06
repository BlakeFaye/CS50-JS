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
            user_listing = form.save(commit=False)
            user_listing.user = request.user
            user_listing.save()
            return redirect('index')
    else:
        form = Auction_Listing_Form()
    return render(request, 'auctions/new_listing.html', {'form': form})


def listing(request, auction_id):
    #Setup des variables
    listing_instance = Auction_Listing.objects.get(pk=auction_id)

    bids = Bid.objects.filter(listing=listing_instance)
    max_bid = list(bids.aggregate(Max("amount", default=0)).values())[0]
    user_max_bid = list(bids.filter(user=request.user).aggregate(Max("amount", default=0)).values())[0]
    
    current_auction_is_open = listing_instance.auction_open
    
    #récup du user
    current_user_is_creator = False
    if request.user == listing_instance.user:
        current_user_is_creator = True
    
    #récup du statut de watchlist
    try:
        Watchlist.objects.get(user=request.user, auctions=listing_instance)
        is_watchlisted = True
    except Watchlist.DoesNotExist:
        is_watchlisted = False

    #initialisation des formulaires
    listing_price = listing_instance.price
    bid_form = Bid_Form(request.POST, max_bid, listing_price)

    listing_form = Auction_Listing_Form(request.POST, instance=listing_instance)  
    listing_form_ro = Auction_Listing_Form_RO(request.GET, instance=listing_instance)  

    if request.method == 'POST':
        print("1")

        context = {
            'listing_form': listing_form_ro, 
            'bid_form': Bid_Form(),
            'id': id, 'auction_id':auction_id, 'auction_open':current_auction_is_open, 'user_is_creator':current_user_is_creator,
            'is_watchlisted':is_watchlisted,
            'max_bid' : max_bid, 'user_max_bid':user_max_bid}
        
        #Vérif du submit du bid_form
        if 'place_bid' in request.POST :
             #Validation du bid
            if bid_form.is_valid():
                print("2")
                user_bid = bid_form.save(commit=False)
                user_bid.user = request.user
                user_bid.listing = listing_instance
                user_bid.save()
                return redirect('listing', auction_id=auction_id)
            else:
                print("3")
                context["bid_form"] = bid_form

        #Vérif du submit du listing_form
        #Validation de l'édit du listing
        if 'save_listing' in request.POST :
            if listing_form.is_valid():
                print("4")
                listing_form.save()
                return redirect('listing', auction_id=auction_id)
            else:
                print("5")
                context["listing_form"] = listing_form_ro

        #Si l'un ou l'autre n'est pas bon, réafficher la page en passant
        #en paramètre le form rempli pour afficher les bonnes données
        #et le message d'erreur
        print("6")
        return render(request,'auctions/listing.html', context)

    else : #GET
        context = {
                'listing_form': listing_form_ro,
                'id': id, 'auction_id':auction_id, 'auction_open':current_auction_is_open, 'user_is_creator':current_user_is_creator,
                'max_bid' : max_bid}
        
        # Cas 1 : Pour modifer son auction encore ouverte
        if current_user_is_creator and current_auction_is_open: 
            context["listing_form"] =  Auction_Listing_Form(instance=listing_instance)

        # Cas 2 : Pour bid sur une auction ouverte
        elif current_auction_is_open:
            context["listing_form"] =  listing_form_ro
            context["bid_form"] =  Bid_Form()
            context["is_watchlisted"] =  is_watchlisted
            context["user_max_bid"] =  user_max_bid

        # Cas 3 : Le + de restrictions, auction fermée normalement, on peut juste consulter
        else:
            context["is_watchlisted"] =  is_watchlisted
    
        return render(request,'auctions/listing.html', context)
        
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


def closeAuction(request, auction_id):
    listing_instance = Auction_Listing.objects.get(pk=auction_id)
    listing_instance.auction_open = False
    listing_instance.save()
    current_user = request.user
    return render(request, "auctions/listings.html", {
    "listings": Auction_Listing.objects.all(),
    'current_user':current_user
    })