from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.createlisting,name="createlisting"),
    path("categorydisplay",views.categorydisplay,name="categorydisplay"),
    path("listing/<str:title>",views.listing,name="listing"),
    path("removefromwatchlist/<str:title>",views.removefromwatchlist,name="removefromwatchlist"),
    path("addtowatchlist/<str:title>",views.addtowatchlist,name="addtowatchlist"),
    path("watchlist/",views.watchlist,name="watchlist"),
    path("comments/<str:title>",views.comments,name="comments"),
    path("addbid/<str:title>",views.addbid,name="addbid"),
    path("auctionclose/<str:title>",views.auctionclose,name="auctionclose")
]
