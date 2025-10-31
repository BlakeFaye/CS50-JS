from django.contrib.auth.models import AbstractUser
from django.db import models    


class User(AbstractUser):
   pass

CATEGORY_OPTIONS = [
    ("fashion", "Fashion"),
    ("toys", "Toys"),
    ("electronics", "Electronics"),
    ("home", "Home"),
    ("other", "Other")
    ]

class Auction_Listing(models.Model):
    title = models.CharField(max_length=240)
    price = models.FloatField()
    user = models.ForeignKey(User, related_name="auction_user", on_delete=models.CASCADE)
    category = models.CharField(max_length=300, choices=CATEGORY_OPTIONS, default="other")
    description = models.TextField(max_length=1000)
    picture = models.URLField(max_length=300) #TODO
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user} for {self.price}. In category: {self.category} with picture: {self.picture} on the {self.date}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Auction_Listing, related_name="bid_listing", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bid_user", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} had bid {self.amount} for {self.listing} on the {self.date}"


class Comment(models.Model):
    listing = models.ForeignKey(Auction_Listing, related_name="comment_listing", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID : {self.id} {self.user} had commented on {self.lising} on the {self.date} : {self.content}"


class Watchlist(models.Model):
    auctions = models.ForeignKey(Auction_Listing, related_name="auctions_in_watchlist", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="watchlist_user", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('auctions', 'user')

    def __str__(self):
        return f"{self.user}'s watchlist with {self.auctions}"