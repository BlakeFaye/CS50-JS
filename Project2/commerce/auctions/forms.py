from django.forms import ModelForm, ModelChoiceField, Form
from .models import Auction_Listing, User, Bid

class Auction_Listing_Form(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Auction_Listing
        fields = ["title", "price", "user", "category", "description", "picture"]

class Bid_Form(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

#https://python.plainenglish.io/how-to-make-inline-form-fields-read-only-based-on-inline-field-values-in-django-d1b25dca6630
