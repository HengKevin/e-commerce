from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Catagory(models.Model):
    catagory = models.TextField(max_length=60)

    def __str__(self):
        return f"{self.catagory}"

class Listing(models.Model):
    title = models.TextField(max_length=50)
    descriptions = models.TextField(null=True, max_length=300)
    created_date = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(null=True, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, related_name="similar_listings")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_creator_listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title} - {self.starting_bid}"

class Picture(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="get_pictures")
    picture = models.ImageField(upload_to="images/")
    alt_text = models.CharField(max_length=50)

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="get_comments")

    def get_creation_date(self):
        return self.created_date.strftime('%B %d %Y')