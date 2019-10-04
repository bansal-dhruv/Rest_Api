from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.db.models import Q
import json
import pdb
import threading

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import action
from webapp.models import *
from webapp.serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.decorators import action
import datetime
from django.contrib.auth.models import User,auth
import schedule
import multiprocessing
# import time
# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import FilterSet
# from django_filters import rest_framework as filters

def Check_Auction():
    while True:
        print('Threading')
        instance = Auction.objects.all()
        auctions = AuctionSerializer(instance,many=True)
        now=str(datetime.datetime.now())
        print(now)
        now_date=int(str(now[0:4]+now[5:7]+now[8:10]))
        now_time=int(str(now[11:13]+now[14:16]))
        print(now_time)
        for auction in auctions.data:
            now = (auction['end_date'])
            date=int(str(now[0:4]+now[5:7]+now[8:10]))
            time=int(str(now[11:13]+now[14:16]))
            if(date<now_date) or (date==now_date and time<=now_time):
                data = {'title': auction['title'], 'description': auction['description'],'start_date':auction['start_date'],'end_date':auction['end_date'],'amount':auction['amount'],'username':auction['username'],'status':'sold'}
                print(data)
                serial = AuctionSerializer(tell_object(auction['title']),data=data)
                if(serial.is_valid()):
                    serial.save()   

        import time
        time.sleep(300)


t=threading.Timer(1,Check_Auction)
t.daemon=True
t.start()
print("Started Thread")

@csrf_exempt
def register(request):
    if request.method == "POST":
        data=json.loads(request.body.decode('utf-8'))
        username=data.get('username')
        print(username)
        password=data.get('password')
        print(password)
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email') 
        try:
            new_user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            new_user.save()
            return JsonResponse( {"Response": "Registration success."}, status=404)
        except :
            return JsonResponse( {"error": "Registration failed due to wrong format or same info."}, status=404)
       


@csrf_exempt
def login(request):
    if request.method == "POST":
        data=json.loads(request.body.decode('utf-8'))
        # pdb.set_trace()
        username=data.get('username')
        print(username)
        password=data.get('password')
        print(password)
       
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            request.session['username']=username
            return JsonResponse( {"Response": "Login success."}, status=404)
        else:
            return JsonResponse( {"error": "Login failed."}, status=404)

@csrf_exempt
def logout(request):
    permission_classes = [IsAuthenticated]
    if request.method == "POST":
        data=json.loads(request.body.decode('utf-8'))
        # pdb.set_trace()
        username=data.get('username')
        print(username)
        password=data.get('password')
        print(password)
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.logout(request)
            request.session['username']="None"
            return JsonResponse( {"Response": "Logout success."}, status=404)
        else:
            return JsonResponse( {"error": "Logout failed."}, status=404)
        

class AddAuctionAPIView(APIView):    
    permission_classes = [IsAdminUser]
    def post(self, request):
        data = request.data
        serializer = AuctionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)
   

class AuctionAPIView(APIView):
    def get(self, request):
        auctions = Auction.objects.all()
        serailizer = AuctionSerializer(auctions, many=True)
        return Response(serailizer.data, status=200)
   

class AuctionDetailView(APIView):
    def get_object(self, title):
        try:
            return Auction.objects.get(title=title)
        except Auction.DoesNotExist as e:
            return Response( {"error": "Given title object not found."}, status=404)

    def get(self, request, title=None):
        instance = self.get_object(title=title)
        serailizer = AuctionSerializer(instance)
        try :
            serailizer.data
            if serailizer.data['status']=='unsold':
                info={'status':'unsold','highest_bid':serailizer.data['amount']}
                return Response(info)
            else:
                info={'status':'sold','highest_bid':serailizer.data['amount'],'highest_bidder': serailizer.data['winner']}
                return Response(info)
        except:
            return Response( {"error": "No bid by this title."}, status=404)
        # if serailizer.data['status']=='unsold':
        #     info={'status':'unsold','highest_bid':serailizer.data['amount']}
        #     return Response(info)
        # else:
        #     info={'status':'sold','highest_bid':serailizer.data['amount'],'highest_bidder': serailizer.data['winner']}
        #     return Response(info)
        # return Response( {"error": "No bid by this user."}, status=404)


class Get_BidView(APIView):
    permission_classes = [IsAuthenticated]
    # request.user.is_authenticated
    def get_object(self,username):
        try:
            return Bids.objects.all().filter(username=username)
        except Bids.DoesNotExist as e:
            return Response( {"error": "No bid by this user."}, status=404)

    def get(self, request, username=None):
        instance = self.get_object(username=username)
        serailizer = BidSerializer(instance,many=True)
        print(serailizer.data)
        # if(serailizer.data['title']==None):
        #     return Response( {"error": "No bid by this user."}, status=404)
        return Response(serailizer.data)

def tell_object(title):         
    return (Auction.objects.get(title=title))
    

# @csrf_exempt
def post_object(title):         
    try:
        return AuctionSerializer(Auction.objects.get(title=title))
    except Auction.DoesNotExist as e:
        return Response( {"error": "No Auction by this title."}, status=404)



@csrf_exempt
def poll(request):   
    permission_classes = [IsAuthenticated]

    if (request.session['username']) == "None":
        return JsonResponse( {"error": "Login to add Bid."}, status=404)

    elif request.method == "POST":        
        print('yes')
        json_parser = JSONParser()
        data = json_parser.parse(request)
        print(data)
        if (request.session['username']) != data['username']:
            return JsonResponse( {"error": "Login to add Bid."}, status=404)
        serializer = Bid2Serializer(data=data)
        print(serializer)
        if serializer.is_valid():

            print(serializer.validated_data)
            title=serializer.validated_data['title']
            amount=serializer.validated_data['amount']
            instance = (post_object(title=title))
            print(instance.data)

            if ('error') in (instance.data) :
                return JsonResponse( {"error": "no item by ths name."}, status=404)
            elif( instance.data['status']!='sold' and amount > instance.data['amount'] ):
                serializer.save()
                # instance.data['amount']=amount
                # instance.data['winner']=serializer.data['username']
                data = {'title': instance.data['title'], 'description': instance.data['description'],'start_date': instance.data['start_date'],'end_date':instance.data['end_date'],'amount':amount,'username':serializer.data['username'],'status':'unsold'}
                print(data)
                serial = AuctionSerializer(tell_object(title),data=data)
                if(serial.is_valid()):
                    serial.save()
                                   
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse( {"error": "Apply with higher bid or Auction has ended."}, status=404)
            
        return JsonResponse(serializer.erros, status=400)

# @csrf_exempt
# def poll(request):
#     if request.method == "POST":
#         return JsonResponse( {"error": "Apply with higher bid or Auction has ended."}, status=404)