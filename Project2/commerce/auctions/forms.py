from django.forms import ModelForm, ModelChoiceField, Form, ValidationError
from .models import Auction_Listing, User, Bid
from django.db import models  

class Auction_Listing_Form(ModelForm):
    class Meta:
        model = Auction_Listing
        fields = ["title", "price", "category", "description", "picture"]

class Auction_Listing_Form_RO(ModelForm):
    class Meta:
        model = Auction_Listing
        fields = ["title", "price", "user", "category", "description", "picture"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].disabled = True
        self.fields["price"].disabled = True
        self.fields["user"].disabled = True
        self.fields["category"].disabled = True
        self.fields["description"].disabled = True
        self.fields["picture"].disabled = True

class Bid_Form(ModelForm):

    max_bid = 0

    #Constructeur pour pouvoir passer une requête et un bid max éventuels pour récupérer le max bid pour l'auction du contexte
    def __init__(self, request=None, max=0, base_price=0):
        super().__init__(request)
        self.max_bid = max
        self.base_price = base_price

    def clean(self):
        cleaned_data=super(Bid_Form, self).clean()
        if self.max_bid >= cleaned_data.get("amount"):
            raise ValidationError("The amount must be superior to max bid")
        if self.base_price >= cleaned_data.get("amount"):
            raise ValidationError("The amount must be superior to the listing base price")
        
    class Meta:
        model = Bid
        fields = ["amount"]

