from rest_framework import serializers
from django.contrib.auth.models import User,auth
from webapp.models import *


class AuctionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "amount",
            "username",
            "status"
            
        ]
        # read_only_fields = ["tags"]

class BidSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bids
        fields = [
            "title",
            "username",
            "amount",
            "status"            
        ]

class Bid2Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bids
        fields = [
            "title",
            "username",
            "amount"            
        ]

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = [
            "username",
            "password"            
        ]