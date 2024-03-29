from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Category,Listing,Comment,Bid


def index(request):
    allcategories=Category.objects.all
    return render(request, "auctions/index.html",{
    "listings":Listing.objects.filter(isactive=True),
    "categories":allcategories
    })

@login_required
def addbid(request,title):
    userbid=int(request.POST['bid'])
    currentuser=request.user
    listingdata=Listing.objects.get(title=title)
    listingdatanew=Listing.objects.filter(isactive=True,title=title) 
    iscurrentuser=request.user.username == listingdata.owner.username
    addedcomments=Comment.objects.filter(listing=listingdata)
    listinginwatchlist=request.user in listingdata.watchlist.all()
    if userbid>listingdata.price.bid:
        updatedbid=Bid(bid=userbid,user=currentuser)
        updatedbid.save()
        listingdata.price=updatedbid
        listingdata.save()
        return render(request,"auctions/listing.html",{
            "listings":listingdatanew,
            "message":"Bid Updated successfully",
            "updatestatus":True,
            "listinginwatchlist":listinginwatchlist,
            "addedcomments":addedcomments,
            "iscurrentuser":iscurrentuser
        })
    else:
        return render(request,"auctions/listing.html",{
            "listings":listingdatanew,
            "message":"Bid Update Failed",
            "updatestatus":False,
            "listinginwatchlist":listinginwatchlist,
            "addedcomments":addedcomments,
            "iscurrentuser":iscurrentuser

        })

@login_required
def auctionclose(request,title):
    listingdata=Listing.objects.get(title=title)
    listingdata.isactive=False
    listingdata.save()
    listingdatanew=Listing.objects.filter(title=title) 
    iscurrentuser=request.user.username == listingdata.owner.username
    addedcomments=Comment.objects.filter(listing=listingdata)
    listinginwatchlist=request.user in listingdata.watchlist.all()
    return render(request,"auctions/listing.html",{
        "listings":listingdatanew,
        "listinginwatchlist":listinginwatchlist,
        "addedcomments":addedcomments,
        "iscurrentuser":iscurrentuser,
        "updatestatus":True,
        "message":"Your auction has been successfully closed."
    })

@login_required
def comments(request,title):
    currentuser=request.user
    listingdata=Listing.objects.get(title=title)
    usercomment=request.POST['comment']
    newcomment= Comment(author=currentuser,listing=listingdata,commentdata=usercomment)
    newcomment.save()
    return HttpResponseRedirect(reverse("listing",args=(title, )))

@login_required
def categorydisplay(request):
    if request.method=="POST":
        allcategories=Category.objects.all
        selectedcategory=request.POST['category']
        category=Category.objects.get(categoryname=selectedcategory)
        return render(request, "auctions/category.html",{
        "listings":Listing.objects.filter(isactive=True,category=category),
        "categories":allcategories,
        })
    else:
        allcategories=Category.objects.all()
        return render(request,"auctions/category.html",{
            "categories":allcategories
        })
    
@login_required
def listing(request,title):
    if request.method=="GET":
        currentuser=request.user
        listingdata=Listing.objects.filter(title=title)
        listingdatanew=Listing.objects.get(title=title)
        addedcomments=Comment.objects.filter(listing=listingdatanew)
        listinginwatchlist=request.user in listingdatanew.watchlist.all()
        iscurrentuser=request.user.username == listingdatanew.owner.username
        return render(request,"auctions/listing.html",{
            "listings":listingdata,
            "listinginwatchlist":listinginwatchlist,
            "addedcomments":addedcomments,
            "currentuser":currentuser,
            "iscurrentuser":iscurrentuser
        })
@login_required
def removefromwatchlist(request,title):
    listingdata=Listing.objects.get(title=title)
    currentuser=request.user
    listingdata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(listingdata.title,)))

@login_required
def addtowatchlist(request,title):
    listingdata=Listing.objects.get(title=title)
    currentuser=request.user
    listingdata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(listingdata.title,)))

@login_required
def watchlist(request):
    currentuser=request.user
    listings=currentuser.watchlistlisting.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })

@login_required
def createlisting(request):
    if request.method=="GET":
        allcategories=Category.objects.all
        return render(request,"auctions/createlisting.html",{
            "categories":allcategories
        })
    else:
        title=request.POST["title"]
        price=request.POST["price"]
        description=request.POST["description"]
        imageurl=request.POST["imageurl"]
        category=request.POST["category"]
        currentuser=request.user
        # isactive=request.POST['isactive']
        categorydata=Category.objects.get(categoryname=category)
        bid=Bid(bid=int(price),user=currentuser)
        bid.save()
        create=Listing(
            title=title,
            price=bid,
            description=description,
            imageurl=imageurl,
            owner=currentuser,
            category=categorydata
        )
        create.save()

        return HttpResponseRedirect(reverse("index"))
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
