from django.contrib import admin
from .models import Nutrient, NutrientGroup, LinkNutrientFood, Database, NutrientNeeds, MapNutrientCodeDatabase, LinkNutrientNutrient
# Register your models here.

class NutrientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nameFr', 'nameEn')

admin.site.register(Nutrient, NutrientAdmin)



admin.site.register(NutrientGroup)
admin.site.register(LinkNutrientFood)
admin.site.register(Database)

class NutrientNeedsAdmin(admin.ModelAdmin):
    list_display = ('id', 'nutrient', 'sex', 'need', 'code')

admin.site.register(NutrientNeeds, NutrientNeedsAdmin)



class MapNutrientCodeDatabaseAdmin(admin.ModelAdmin):
    list_display = ('nutrient', 'nutrient_code')

admin.site.register(MapNutrientCodeDatabase, MapNutrientCodeDatabaseAdmin)


class LinkNutrientNutrientAdmin(admin.ModelAdmin):
    list_display = ('mom_nutrient', 'son_nutrient')

admin.site.register(LinkNutrientNutrient, LinkNutrientNutrientAdmin)