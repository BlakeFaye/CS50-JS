from django.contrib import admin
from .models import User, Bid, Auction_Listing, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Auction_Listing)
admin.site.register(Comment)
