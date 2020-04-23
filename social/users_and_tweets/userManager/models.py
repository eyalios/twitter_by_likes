from django.contrib.postgres.fields import  ArrayField
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class SimpleUser(models.Model):
    userName            = models.TextField()
    password            = models.TextField()
    email               = models.TextField()
    favorites           = models.TextField()
    access_token        = models.TextField(default="")
    access_token_secret = models.TextField(default="")

class UserTweeter(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    access_token = models.TextField(default="")
    access_token_secret = models.TextField(default="")
    friends = models.TextField(default="")