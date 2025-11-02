from django.forms import ModelForm, ModelChoiceField, Form, ValidationError
from .models import Auction_Listing, User, Bid
from django.db import models  

class Auction_Listing_Form(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Auction_Listing
        fields = ["title", "price", "user", "category", "description", "picture"]

class Bid_Form(ModelForm):

    max_bid = 0

    #Constructeur pour pouvoir passer une requête et un bid max éventuels pour récupérer le max bid pour l'auction du contexte
    def __init__(self, request=None, max=0):
        super().__init__(request)
        self.max_bid = max

    def clean(self):
        cleaned_data=super(Bid_Form, self).clean()
        if self.max_bid >= cleaned_data.get("amount"):
            raise ValidationError("The amount must be superior to max bid")
        
    class Meta:
        model = Bid
        fields = ["amount"]

#https://python.plainenglish.io/how-to-make-inline-form-fields-read-only-based-on-inline-field-values-in-django-d1b25dca6630
