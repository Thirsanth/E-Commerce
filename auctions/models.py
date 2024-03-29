from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    categoryname=models.CharField(max_length=64)

    def __str__(self):
        return self.categoryname

class Bid(models.Model):
    bid=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userbid")


class Listing(models.Model):
    title=models.CharField(max_length=64)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,blank=True,null=True,related_name="biddingprice")
    description=models.CharField(max_length=200)
    imageurl=models.CharField(max_length=1500)
    isactive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="watchlistlisting")
    def __str__(self):
        return self.title

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="usercomment")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="listingcomment")
    commentdata=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
    

