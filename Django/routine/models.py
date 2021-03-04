from django.db import models
from django.contrib.auth.models import User
from meal.models import Meal

# Create your models here.
class Routine(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User,  on_delete=models.SET_DEFAULT, default=None, null=True)







class RoutineList(models.Model):
    user = models.ForeignKey(User,  on_delete=models.SET_DEFAULT, default=None, null=True)
    routine = models.ForeignKey(Routine,  on_delete=models.SET_DEFAULT, default=None, null=True)




class Link_routine_meal(models.Model):
    routine = models.ForeignKey(Routine,  on_delete=models.SET_DEFAULT, default=None, null=True)
    meal = models.ForeignKey(Meal,  on_delete=models.SET_DEFAULT, default=None, null=True)
    consumption_hour = models.IntegerField(default = 0)



