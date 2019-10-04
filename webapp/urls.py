from django.contrib import admin
from django.urls import path,include
from webapp.views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

# router = DefaultRouter()
# router.register('webapp', AuctionAPIView)

urlpatterns = [
	path('/AddBid/', poll),					#post
	path('/register/', register),			#post
	path('/login/', login),					#post
	path('/logout/', logout),				#post
	path('/', AuctionAPIView.as_view()),	#get
	path('/<slug:title>/',  AuctionDetailView.as_view()),	#get
	path('/Bid/<slug:username>/',  Get_BidView.as_view()),	#get
	path('/add/', AddAuctionAPIView.as_view()),				#post by admin only
]