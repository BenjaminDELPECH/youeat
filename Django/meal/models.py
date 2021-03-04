from django.contrib.auth.models import User
from django.db import models

from foods.models import Food
from foods.models import ConversionFactor


# Create your models here.
class Object_type(models.Model):
    name = models.CharField(max_length=255)

class Meal(models.Model):
    name = models.CharField(max_length=149)
    object_type = models.ForeignKey(Object_type, on_delete=models.CASCADE, null=False, default =2)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)

    scrapped = models.BooleanField(default=False)

    preparationTime = models.CharField(max_length=150, default="1h20")
    difficulty = models.IntegerField(default=0)
    imgUrl = models.URLField(default="https://assets.afcdn.com/recipe/20150901/59954_w420h344c1cx1500cy2250.jpg")

    nutrientDensity = models.FloatField(default=0)
    glycemicLoad = models.FloatField(default=20)
    immuneSystemScore = models.FloatField(default=2)
    testosteroneScore = models.FloatField(default=2)
    bonesScore = models.FloatField(default=2)


class LinkMealMeal(models.Model):
    mom_meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='father_meal', null=True, default =None)
    son_meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True, related_name='son_meal',default =None)

class LinkMealRoutineProp(models.Model):
    linkMealMeal = models.ForeignKey(LinkMealMeal, on_delete=models.CASCADE, null=True, default =None)
    consumption_hour = models.FloatField(default=0)


class Link_object_page(models.Model):
    page_path =  models.CharField(max_length=255)
    object_type = models.ForeignKey(Object_type, on_delete=models.CASCADE)


class Unit(models.Model):
    name = models.CharField(max_length=255)
    conversion_ratio = models.FloatField()


class Link_meal_food(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.SET_DEFAULT, default=None, null=True)
    food = models.ForeignKey(Food, on_delete=models.SET_DEFAULT, default=None, null=True)
    food_name_scrapped = models.CharField(max_length=255, default="")
    quantity = models.FloatField(default=50)

    conversion_factor = models.ForeignKey(ConversionFactor,  on_delete=models.SET_DEFAULT, default=None, null=True)



class Link_meal_user(models.Model):
    meal = models.ForeignKey(Meal,  on_delete=models.SET_DEFAULT, default=None, null=True)
    user = models.ForeignKey(User,  on_delete=models.SET_DEFAULT, default=None, null=True)
