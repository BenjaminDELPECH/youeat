from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    ip_adress = models.CharField(default="", max_length=255)
    sexe = models.IntegerField(default=1)
    age = models.IntegerField(default=35)
    taille = models.IntegerField(default=175)
    poid = models.IntegerField(default=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.FloatField(default = 1.2)
    carbohydrateProportion = models.FloatField(default=50)
    fatProportion = models.FloatField(default=35)
    proteinProportion = models.FloatField(default=15)
    social_account = models.BooleanField(default=0)
    anonyme_account = models.BooleanField(default=None, null=True)
    activation_token = models.CharField(max_length=255,default=None, null=True)
    activation_code_forget_password = models.IntegerField(default=None, null=True)