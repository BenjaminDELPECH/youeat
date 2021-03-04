import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from foods.models import Food, FoodGroup
from meal.models import Link_meal_food, LinkMealMeal
from routine.models import Link_routine_meal
from nutrients.models import *
from django.db.models import Max


class LinkNutrientFoodType(DjangoObjectType):
    class Meta:
        model = LinkNutrientFood


class NutrientType(DjangoObjectType):
    class Meta:
        model = Nutrient


class LinkNutrientNutrientType(DjangoObjectType):
    class Meta:
        model = LinkNutrientNutrient


class NutrientsGroupType(DjangoObjectType):
    class Meta:
        model = NutrientGroup


class NutrientCategoryType(DjangoObjectType):
    class Meta:
        model = NutrientCategory


class NutrientCategoryRoleType(DjangoObjectType):
    class Meta:
        model = NutrientCategoryRole


class NutrientBestFoodType(graphene.ObjectType):
    nutrient_id = graphene.Int()
    food_id = graphene.Int()
    value = graphene.Float()
    cat = graphene.Int()

class NutrientNeeds(DjangoObjectType):
    class Meta:
        model = NutrientNeeds


class Query(object):
    nutrients = graphene.List(NutrientType)
    nutrients_group = graphene.List(NutrientsGroupType)
    nutrient = graphene.Field(NutrientType, nutrient_id=graphene.Int())
    linkNutrient = graphene.Field(LinkNutrientFoodType, food_id=graphene.Int(), nutrient_id=graphene.Int())
    linkNutrientFoodList = graphene.List(LinkNutrientFoodType, food_id=graphene.Int())
    linkNutrientFoodSetList = graphene.List(graphene.List(LinkNutrientFoodType), mealId=graphene.Int())

    linkNutrientsFood = graphene.List(LinkNutrientFoodType, food_id_list=graphene.List(graphene.Int),
                                      meal_id=graphene.Int(),
                                      nutrient_id=graphene.Int())

    linkNutrientsByFoodListAndRoutineId = graphene.List(LinkNutrientFoodType,
                                                        nutrient_id_list=graphene.List(graphene.Int),
                                                        routine_id=graphene.Int(),
                                                        food_id=graphene.Int())

    nutrientCategories = graphene.List(NutrientCategoryType)
    nutrientBestFoods = graphene.List(NutrientBestFoodType, nutrient_id=graphene.Int(required=True))
    allNutrientsBestFood = graphene.List(graphene.List(NutrientBestFoodType))


    @staticmethod
    def resolve_allNutrientsBestFood(self, info):
        nutrients = Nutrient.objects.filter(besoin__gt=0).exclude(nutrientGroup=None, besoin=None)
        list = []
        food_groups = FoodGroup.objects.all().exclude(id=2)
        for nutrient in nutrients:
            obj =getNutrietBestFoodForOneNutrientId(food_groups, nutrient_id=nutrient.id)

            # dict_obj = [{"cat": elem.cat, "foodId": elem.food_id, "nutrientId": elem.nutrient_id,
            #              "value": float(str(elem.value))} for elem in obj]
            list.append(obj)

        # import json
        # file_name = "nutrientBestFoods.json"
        # with open(file_name, 'w+', encoding='utf-8') as f:
        #     json.dump(list, f, ensure_ascii=False, indent=4)

        return list

    @staticmethod
    def resolve_nutrientBestFoods(self, info, nutrient_id):
        food_groups = FoodGroup.objects.all()
        return getNutrietBestFoodForOneNutrientId(food_groups, nutrient_id)




    @staticmethod
    def resolve_nutrientCategories(self, info):
        return NutrientCategory.objects.all().exclude(activated = False)

    @staticmethod
    def resolve_nutrients_group(self, info):
        return NutrientGroup.objects.all()

    def resolve_linkNutrientsFood(self, info, food_id_list=None, meal_id=None, nutrient_id=None):
        if meal_id:
            meal_id_list = list(LinkMealMeal.objects.filter(mom_meal_id=meal_id).values_list('son_meal_id', flat=True))
            meal_id_list.append(meal_id)

            food_id_list = Food.objects.filter(link_meal_food__meal__in=meal_id_list).values_list('id', flat=True)

        result = LinkNutrientFood.objects.filter(food_id__in=food_id_list)

        if nutrient_id:
            result = result.filter(nutrient_id=nutrient_id)
        return result

    def resolve_linkNutrientsByFoodListAndRoutineId(self, info, nutrient_id_list, routine_id=None, food_id=None):
        food_id_list = []
        if routine_id:
            link_routine_meal_id_list = Link_routine_meal.objects.filter(routine_id=routine_id).values_list('meal_id')
            food_id_list = Link_meal_food.objects.filter(meal_id__in=link_routine_meal_id_list).values_list('food_id')
        else:
            food_id_list.append(food_id)
        return LinkNutrientFood.objects.filter(food_id__in=food_id_list,
                                               nutrient_id__in=nutrient_id_list)

    def resolve_linkNutrientFoodSetList(self, info, mealId):
        linkNutrientFoodSetList = []
        food_id_list = Link_meal_food.objects.filter(meal_id=mealId).values_list('food_id', flat=True).distinct()
        for food_id in food_id_list:
            links = LinkNutrientFood.objects.filter(food_id=food_id)
            linkNutrientFoodSetList.append(links)

        return linkNutrientFoodSetList

    def resolve_linkNutrient(self, info, nutrient_id, food_id):
        if LinkNutrientFood.objects.filter(nutrient_id=nutrient_id, food_id=food_id).count() > 0:
            return LinkNutrientFood.objects.get(nutrient_id=nutrient_id, food_id=food_id)
        else:
            raise GraphQLError("There is not link nutrient food for this nutrient and food id")

    def resolve_nutrient(self, info, nutrient_id):
        return Nutrient.objects.get(id=nutrient_id)

    def resolve_linkNutrientFoodList(self, info, food_id):
        if food_id:
            links = LinkNutrientFood.objects.filter(food_id=food_id)
        else:
            links = LinkNutrientFood.objects.all()
        return links.distinct()

    def resolve_nutrients(self, info):
        return Nutrient.objects.all()


class CreateNutrient(graphene.Mutation):
    nutrient = graphene.Field(NutrientType)

    class Arguments:
        id = graphene.Int()
        nameEn = graphene.String()
        nameFr = graphene.String()
        unit = graphene.String()

    def mutate(self, info, id, nameEn, nameFr, unit):
        if Nutrient.objects.filter(id=id).count():
            nutrient = Nutrient.objects.get(id=id)
            nutrient.nameEn = nameEn
            nutrient.nameFr = nameFr
            nutrient.unit = unit
            nutrient.save()
        else:
            nutrient = Nutrient(id=id, nameEn=nameEn, nameFr=nameFr, unit=unit)
            nutrient.save()
        return CreateNutrient(nutrient=nutrient)


class CreateLinkNutrientFood(graphene.Mutation):
    linkNutrientFood = graphene.Field(LinkNutrientFoodType)

    class Arguments:
        food_id = graphene.Int()
        nutrient_id = graphene.Int()
        nutrient_name = graphene.String()
        value = graphene.Float()

    def mutate(self, info, food_id, nutrient_id, value):
        print(food_id)
        print(nutrient_id)
        if Food.objects.filter(id=food_id).count():
            if Nutrient.objects.filter(id=nutrient_id).count():
                link_id = int(str(food_id) + str(nutrient_id))
                if LinkNutrientFood.objects.filter(id=link_id).count() == 0:
                    value = float(value)
                    linkNutrientFood = LinkNutrientFood(id=link_id, food_id=food_id, nutrient_id=nutrient_id,
                                                        value=value)
                    linkNutrientFood.save()
                # fusion de la vitamine k1 present dans base cliqual avec la vitamine k2
                elif nutrient_id == 430:
                    linkNutrientFood = LinkNutrientFood.objects.get(id=link_id)
                    linkNutrientFood.value += float(value)
                    linkNutrientFood.save()
                else:
                    raise GraphQLError("This food nutrient link already exist motherfucker")
            else:
                raise GraphQLError("This Nutrient fucking not exist motherFucker")
        else:
            raise GraphQLError("This food fucking not exist motherFucker, foodId :" + str(food_id))

        return CreateLinkNutrientFood(linkNutrientFood=linkNutrientFood)


class UpdateLinkNutrientFood(graphene.Mutation):
    linkNutrientFood = graphene.Field(LinkNutrientFoodType)

    class Arguments:
        food_id = graphene.Int()
        nutrient_id = graphene.Int()
        value = graphene.Float()

    def mutate(self, info, food_id, nutrient_id, value):
        links = LinkNutrientFood.objects.filter(food_id=food_id)
        link = None
        if links.count() >= 1:
            links = links.filter(nutrient_id=nutrient_id)
            if links.count() == 1:
                link = LinkNutrientFood.objects.get(food_id=food_id, nutrient_id=nutrient_id)
                link.value = value
                link.save()

            elif links.count() == 0:
                return CreateLinkNutrientFood.mutate(self, info, food_id=food_id, nutrient_id=nutrient_id, value=value)
            else:
                raise GraphQLError(
                    "more than one link nutrient food for this food id and nutrien id, should be just one")
        else:
            link = LinkNutrientFood(food_id=food_id, nutrient_id=nutrient_id)
            link.save()

        return UpdateLinkNutrientFood(linkNutrientFood=link)


class UpdateOrCreateLinkNutrientByFoodModel(graphene.Mutation):
    linkNutrientFoodList = graphene.List(LinkNutrientFoodType)

    class Arguments:
        food_id_to_update = graphene.Int()
        food_id_model = graphene.Int()
        nutrient_title_id = graphene.Int()

    def mutate(self, info, food_id_to_update, food_id_model, nutrient_title_id):
        linksModel = LinkNutrientFood.objects.filter(food_id=food_id_model,
                                                     nutrient__nutrienttitle__nutrientGroup_id=nutrientGroupId)
        nutrientTitleFoodModelQt = LinkNutrientFood.objects.get(nutrient_id=nutrient_title_id,
                                                                food_id=food_id_model).value
        nutrientTitleFoodToUpdateQt = LinkNutrientFood.objects.get(nutrient_id=nutrient_title_id,
                                                                   food_id=food_id_to_update).value
        for link in linksModel:
            ratio = link.value / nutrientTitleFoodModelQt
            new_nutrient_val = nutrientTitleFoodToUpdateQt * ratio
            print(new_nutrient_val)
            # Update or create
            if LinkNutrientFood.objects.filter(nutrient_id=link.nutrient_id, food_id=food_id_to_update).count() > 1:
                raise GraphQLError(
                    "It should not exist more than one link nutrient food for this food id and nutrient id")
            elif LinkNutrientFood.objects.filter(nutrient_id=link.nutrient_id, food_id=food_id_to_update).count() == 1:
                link_to_update = LinkNutrientFood.objects.get(nutrient_id=link.nutrient_id, food_id=food_id_to_update)
                link_to_update.value = new_nutrient_val
                link_to_update.save()
            else:
                link_to_create = LinkNutrientFood(nutrient_id=link.nutrient_id, food_id=food_id_to_update,
                                                  value=new_nutrient_val)
                link_to_create.save()

        return UpdateOrCreateLinkNutrientByFoodModel(linkNutrientFoodList=linksModel)


class Mutation(graphene.ObjectType):
    create_nutrient = CreateNutrient.Field()
    create_link_nutrient_food = CreateLinkNutrientFood.Field()
    updateLinkNutrientFood = UpdateLinkNutrientFood.Field()
    updateOrCreateLinkNutrientByFoodModel = UpdateOrCreateLinkNutrientByFoodModel.Field()



def getNutrietBestFoodForOneNutrientId(food_groups, nutrient_id):
    nutrientBestFoodType_list = []
    food_groups_scores = []
    for food_group in food_groups:

        food_group_score = 0
        food_id_list = Food.objects.filter(foodGroup=food_group)
        lnfs = LinkNutrientFood.objects.filter(food_id__in=food_id_list, nutrient_id=nutrient_id).order_by(
            '-value')[:25]
        if len(lnfs) > 0:
            besoin = lnfs[0].nutrient.besoin
            for lnf in lnfs:
                try:
                    percentage = float(lnf.value) / float(besoin)
                except Exception:
                    print("hello")
                if percentage > 0.05:
                    nutrientBestFoodType = NutrientBestFoodType(food_id=lnf.food.id, nutrient_id=lnf.nutrient.id,
                                                                value=lnf.value, cat=food_group.id)
                    nutrientBestFoodType_list.append(nutrientBestFoodType)
                    food_group_score += percentage

        food_groups_scores.append({"foodGroupId": food_group.id, "score": food_group_score})
    #
    sortedlol = sorted(food_groups_scores, key=lambda e: (e['score']), reverse=True)
    sortedlol = [elem['foodGroupId'] for elem in sortedlol]
    if len(sortedlol) > 0:
        sortedlol = sortedlol[:5]
    nutrientBestFoodType_list = [elem for elem in nutrientBestFoodType_list if elem.cat in sortedlol]
    return nutrientBestFoodType_list
