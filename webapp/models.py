from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

class Auction(models.Model):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    amount = models.PositiveIntegerField()
    username=models.TextField(null=False, blank=False)
    status = models.CharField(default='unsold', max_length=10)  

class Bids(models.Model):
    title = models.CharField(null='False' , max_length=25)  
    username=models.CharField(null='False' , max_length=25) 
    amount = models.PositiveIntegerField(null='False')
    status=models.CharField(default='Inprogress', max_length=25)  

class Bid_user(models.Model):
    username=models.CharField(null='False' , max_length=25)  
    password=models.CharField(null='False' , max_length=25)  
    fullname=models.CharField(null='False' , max_length=25)  
    emailid=models.CharField(null='False' , max_length=25)  