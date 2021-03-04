from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Meal)
admin.site.register(Link_meal_food)
admin.site.register(Link_meal_user)
admin.site.register(Object_type)
admin.site.register(Link_object_page)
