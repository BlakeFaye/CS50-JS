from django.forms import ModelForm, ModelChoiceField
from .models import Auction_Listing, User

class Auction_Listing_Form(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Auction_Listing
        fields = ["title", "price", "user", "category", "description", "picture"]
