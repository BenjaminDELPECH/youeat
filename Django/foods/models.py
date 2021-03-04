from django.db import models

class FoodGroup(models.Model):
    name_en = models.CharField(max_length=150, default="group_name_en")
    name_fr = models.CharField(max_length=150, default="group_name_fr")

    def __str__(self):
        return '%s' % (self.name_fr)


class MapFoodGroup(models.Model):
    # alim_group_level values possible : grp, ss_grp, ss_ss_grp
    CHOICES = (('grp', 'grp'), ('ss_grp', 'ss_grp'), ('ss_ss_grp', 'ss_ss_grp'))
    alim_group_level = models.CharField(max_length=150, choices=CHOICES)
    grp_code = models.CharField(max_length=150)
    food_group= models.ForeignKey(FoodGroup, on_delete=models.CASCADE)



# Create your models here.
class Food(models.Model):
    foodGroup = models.ForeignKey(FoodGroup, on_delete=models.SET_DEFAULT, default=None, null=True)
    name_en = models.CharField(max_length=255, default="food_name_en", null=True)
    name_fr = models.CharField(max_length=253, default="food_name_fr")
    activated = models.BooleanField(default=True, null=True)
    nb_of_selection = models.IntegerField(default=0)


    class Meta:
        indexes = [
            models.Index(fields=['name_fr'])
        ]


class GoogleFoodsLabels(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    img_url = models.URLField(max_length=500, default="")
    label = models.CharField(max_length=250)


class MapMarmittonFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_DEFAULT, default=None, null=True)
    marmitton_food_name = models.CharField(max_length=250, primary_key=True)

    recurrence = models.IntegerField(default=0)
    negligable = models.BooleanField(default=False)


class Measure(models.Model):
    nameFr = models.CharField(max_length=255, default="")
    nameEn = models.CharField(max_length=255, default="")


class ConversionFactor(models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_DEFAULT, default=None, null=True)
    measure = models.ForeignKey(Measure, on_delete=models.SET_DEFAULT, default=None, null=True)
    conversion_factor = models.FloatField()

class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    image = models.BinaryField()
    imgUrl = models.URLField(default=None, null=True)

