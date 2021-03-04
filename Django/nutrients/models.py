from django.db import models

from foods.models import Food


class NutrientGroup(models.Model):
    nameFr = models.CharField(max_length=255, default="")
    nameEn = models.CharField(max_length=255, default="")
    deployed_default = models.BooleanField(default=False)
    position = models.IntegerField(default=0)


class Nutrient(models.Model):
    nameFr = models.CharField(max_length=255, default="nutrient_name_fr_default")
    familiarNameFr = models.CharField(max_length=255, default="")
    nameEn = models.CharField(max_length=255)
    unit = models.SlugField(null=True)
    besoin = models.CharField(default=0, max_length=255)
    besoinMax = models.CharField(default=0, max_length=255)
    menNeed = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    womenNeed = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    max = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    sportivAdditionnalNeed = models.IntegerField(default=0, null=True)
    code = models.CharField(max_length=255, null=True)
    nutrientGroup = models.ForeignKey(NutrientGroup, on_delete=models.SET_DEFAULT, default=None, null=True)
    nutrientGroupTitle = models.BooleanField(default=False)
    needPerKg = models.BooleanField(default=False, null=True)


    def __str__(self):
        label = self.nameFr
        if len(self.familiarNameFr) > 0:
            label = self.familiarNameFr
        return '%s' % (label)


class NutrientNeeds(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    sex = models.IntegerField(default=-1)
    need  = models.FloatField(default=0.0)
    code = models.CharField(default = " ", max_length=255, null = True)



class NutrientCategory(models.Model):
    icon_name = models.CharField(max_length=255)
    category_name_fr = models.CharField(max_length=255)
    category_name_en = models.CharField(max_length=255)
    activated = models.BooleanField(default=True)


class NutrientCategoryRole(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    nutrientCategory = models.ForeignKey(NutrientCategory,on_delete=models.CASCADE, null=True)
    role_fr = models.CharField(max_length=255)
    role_en = models.CharField(max_length=255)


class LinkNutrientNutrient(models.Model):
    mom_nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, related_name='mom_nutrient', null=True,
                                     default=None)
    son_nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, null=True, related_name='son_nutrient',
                                     default=None)
    order = models.IntegerField(default=0)



class LinkNutrientFood(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.SET_DEFAULT, default=None, null=True)
    food = models.ForeignKey(Food, on_delete=models.SET_DEFAULT, default=None, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=5)


class Database(models.Model):
    name = models.CharField(max_length=255)


class MapNutrientCodeDatabase(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE, default=None, null=True)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    nutrient_code = models.IntegerField()
