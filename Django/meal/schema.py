import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
import logging

from django.db.models import Q
from meal.models import *
from foods.models import *
from nutrients.models import LinkNutrientFood
from nutrients.models import *
from nutrients.schema import NutrientType, LinkNutrientFoodType
from routine.models import Link_routine_meal
from routine.schema import LinkRoutineMealType
from foods.models import Measure
import requests as req
import json
import csv
import jellyfish

from utils.User import getUserId

class ListObjectPageType(DjangoObjectType):
    class Meta:
        model = Link_object_page

class ObjectType(DjangoObjectType):
    class Meta:
        model = Object_type

class LinkMealUserType(DjangoObjectType):
    class Meta:
        model = Link_meal_user


class LinkMealFoodType(DjangoObjectType):
    class Meta:
        model = Link_meal_food


class MealType(DjangoObjectType):
    class Meta:
        model = Meal


class UnitType(DjangoObjectType):
    class Meta:
        model = Unit


class ChangeLinkMealFoodType(graphene.ObjectType):
    old_meal_id = graphene.Int()
    food_id = graphene.Int()
    new_meal_id = graphene.Int()


class StatType(graphene.ObjectType):
    sum_value = graphene.Float()
    nutrient = graphene.Field(NutrientType)


class MealStatsType(graphene.ObjectType):
    stats = graphene.List(StatType)

class LinkMealMealType(DjangoObjectType):
    class Meta:
        model = LinkMealMeal

class LinkMealRoutinePropType(DjangoObjectType):
    class Meta:
        model = LinkMealRoutineProp

class Query(object):
    link_meal_user = graphene.List(LinkMealUserType)

    link_meal_meals = graphene.List(LinkMealMealType, meal_id = graphene.Int(required = True))

    link_object_pages = graphene.List(ListObjectPageType)
    meals = graphene.List(MealType, object_type=graphene.Int(required=False), searchText=graphene.String(required=False))
    meal = graphene.Field(MealType, id=graphene.Int(required=True))
    units = graphene.List(UnitType)
    unit = graphene.List(UnitType, text=graphene.String(required=True))
    customMealList = graphene.List(MealType, routineId=graphene.Int())
    linkMealFoodByMealId = graphene.List(LinkMealFoodType, meal_id=graphene.Int(required=True))

    def resolve_link_meal_meals(self, info, meal_id):
        return LinkMealMeal.objects.filter(mom_meal_id = meal_id)

    def resolve_link_object_pages(self, info):
        return Link_object_page.objects.all()

    def resolve_linkMealFoodByMealId(self, info, meal_id):
        son_meal_id_list = LinkMealMeal.objects.filter(mom_meal_id=meal_id).values_list('son_meal_id', flat=True)
        return Link_meal_food.objects.filter(Q(meal_id__in=son_meal_id_list)|Q(meal_id=meal_id))

    def resolve_customMealList(self, info, routineId):
        link_routine_meal_list = Link_routine_meal.objects.filter(routine_id=routineId)
        meal_id_list = []
        for elem in link_routine_meal_list:
            meal_id_list.append(elem.meal.id)

        return Meal.objects.filter(scrapped=False, id__in=meal_id_list)

    def resolve_unit(self, info, text):
        return Unit.objects.filter(name__icontains=text)

    def resolve_units(self, info):
        return Unit.objects.all()





    def resolve_meal(self, info, id):
        return Meal.objects.get(id=id)

    def resolve_meals(self, info, object_type=None, searchText=None):
        user_id = getUserId(info.context)

        meals = Meal.objects.filter(author_id=user_id)
        if object_type:
            meals = meals.filter(object_type_id=object_type)

        if searchText:
            meals = meals.filter(
                Q(name__icontains=searchText)
            )[:100]


        return meals



    def resolve_link_meal_user(self, info):
        user = info.context.user
        if not user.is_anonymous:
            links = Link_meal_user.objects.filter(user_id=user.id)
            return links.distinct()
        else:
            raise GraphQLError("not allowed")


class CreateScrapingMeal(graphene.Mutation):
    meal = graphene.Field(MealType)

    class Arguments:
        name = graphene.String(required=True)
        preparationTime = graphene.String(required=True)
        difficulty = graphene.Int(required=True)
        imgUrl = graphene.String(required=True)

    def mutate(self, info, name, preparationTime, difficulty, imgUrl):
        if Meal.objects.filter(name=name).count() == 0:
            new_meal = Meal(name=name, preparationTime=preparationTime, difficulty=difficulty, imgUrl=imgUrl,
                            scrapped=True)
            new_meal.save()
            return CreateScrapingMeal(meal=new_meal)
        else:
            return None


class CreateCustomMeal(graphene.Mutation):
    newLinkRoutineMeal = graphene.Field(LinkRoutineMealType)

    class Arguments:
        name = graphene.String(required=True)
        routineId = graphene.Int(required=True)
        consumption_hour = graphene.Int(required=False)

    def mutate(self, info, name, routineId, consumption_hour=None):
        createCustomMeal = Meal(name=name)
        createCustomMeal.save()

        if not consumption_hour:
            consumption_hour_final_val = 12
        else:
            consumption_hour_final_val = consumption_hour

        newLinkRoutineMeal = Link_routine_meal(routine_id=routineId, meal_id=createCustomMeal.id,
                                               consumption_hour=consumption_hour_final_val)
        newLinkRoutineMeal.save()

        return CreateCustomMeal(newLinkRoutineMeal=newLinkRoutineMeal)





class CreateMeal(graphene.Mutation):
    meal = graphene.Field(MealType)
    successMessage = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        object_type_id = graphene.Int(required=False)

    @staticmethod
    def mutate(self, info, name,object_type_id=2):
        user_id = getUserId(info.context)
        if user_id ==-1 :
            user_id = None

        new_meal = Meal(name=name, author_id=user_id, object_type_id=object_type_id)

        new_meal.save()
        return CreateMeal(meal=new_meal, successMessage="Your meal has been created succesfully !")

class UpdateMeal(graphene.Mutation):
    meal = graphene.Field(MealType)

    class Arguments:
        id = graphene.Int(required = True)
        name = graphene.String(required = False)

    def mutate(self, info, id, name):
        meal = Meal.objects.get(id = id)
        if name :
            meal.name = name
        meal.save()
        return UpdateMeal(meal = meal)




class CreateLinkMealMeal(graphene.Mutation):
    linkMeals = graphene.List(LinkMealMealType)
    linkNutrientsFoods = graphene.List(LinkNutrientFoodType)

    class Arguments:
        mom_meal_id = graphene.Int(required = True)
        son_id_list = graphene.List(graphene.Int, required = True)

    def mutate(self, info, mom_meal_id, son_id_list):

        linkMeals = []
        food_id_list = Link_meal_food.objects.filter(meal_id__in=son_id_list).values_list('food_id', flat= True)
        linkNutrientsFoods = LinkNutrientFood.objects.filter(food_id__in=food_id_list)
        for son_id in son_id_list:
            # if LinkMealMeal.objects.filter(mom_meal_id= mom_meal_id, son_meal_id=son_id).count()<1:
            new_link = LinkMealMeal(mom_meal_id=mom_meal_id, son_meal_id = son_id)
            new_link.save()
            linkMeals.append(new_link)

            # else:
            #     raise GraphQLError("Son of bitch, you cannot create duplicate LinkMealMeal")

        return CreateLinkMealMeal(linkMeals = linkMeals, linkNutrientsFoods = linkNutrientsFoods)




class UpdateCustomMeal(graphene.Mutation):
    updatedCustomMeal = graphene.Field(MealType)

    class Arguments:
        mealId = graphene.Int(required=True)
        newName = graphene.String()

    def mutate(self, info, mealId, newName=None):
        testCount = Meal.objects.filter(id=mealId).count()
        if testCount == 1:
            obj = None
            if newName:
                obj = Meal.objects.get(id=mealId)
                obj.name = newName

            if obj:
                obj.save()
                return UpdateCustomMeal(updatedCustomMeal=obj)
            else:
                raise GraphQLError("no field to update")
        else:
            raise GraphQLError("There is no meal with this id, or more than one meal")


class DuplicateLinkRoutineMeal(graphene.Mutation):
    oldObjId = graphene.Int()
    duplicateRoutineMeal = graphene.Field(LinkRoutineMealType)

    class Arguments:
        linkRoutineMealId = graphene.Int()

    def mutate(self, info, linkRoutineMealId):
        try:
            linkROutineMeal = Link_routine_meal.objects.get(id=linkRoutineMealId)
            newLinkROutineMEal = linkROutineMeal
            newLinkROutineMEal.id = None
            newMeal = newLinkROutineMEal.meal
            newLinkMealFoodList = Link_meal_food.objects.filter(meal=newMeal)
            newMeal.id = None
            newMeal.save()
            for elm in newLinkMealFoodList:
                elm.id = None
                elm.meal = newMeal
                elm.save()

            newLinkROutineMEal.meal = newMeal
            newLinkROutineMEal.save()

            return DuplicateLinkRoutineMeal(oldObjId=linkRoutineMealId, duplicateRoutineMeal=newLinkROutineMEal)




        except Exception as e:
            logging.exception(e)


class CreateLinkMealFood(graphene.Mutation):
    linkMealFood = graphene.Field(LinkMealFoodType)
    linkNutrientsFood = graphene.List(LinkNutrientFoodType)

    class Arguments:
        meal_id = graphene.Int(required=True)
        food_id = graphene.Int(required=True)
        food_name_scrapped = graphene.String()
        conversion_factor_id = graphene.Int()
        quantity = graphene.Int()

    def mutate(self, info, meal_id, food_id, quantity=1, food_name_scrapped="",conversion_factor_id=None):
        result_nb = Link_meal_food.objects.filter(meal_id=meal_id, food_id=food_id).count()

        if result_nb > 0:
            raise GraphQLError("Vous avez déjà ajouté cet aliment à ce repas")
        else:
            conversion_factor_id_list= ConversionFactor.objects.filter(food_id = food_id).values_list('id', flat=True)
            new_obj = Link_meal_food.objects.create(meal_id=meal_id, food_id=food_id, quantity=quantity,
                                                    food_name_scrapped=food_name_scrapped,
                                                    conversion_factor_id=conversion_factor_id_list[0])
            new_obj.save()
            return CreateLinkMealFood(linkMealFood=new_obj)



class CreateLinkMealFoodList(graphene.Mutation):
    linkMealFoodList = graphene.List(LinkMealFoodType)

    class Arguments:
        meal_id = graphene.Int(required=True)
        food_id_list = graphene.List(graphene.Int, required=True)
        quantity_list = graphene.List(graphene.Float, required=True)
        conversion_factor_id_list = graphene.List(graphene.Int, required=True)
        food_name_scrapped = graphene.String()

    def mutate(self, info, meal_id, food_id_list, quantity_list, conversion_factor_id_list, food_name_scrapped=""):

        new_link_meal_food_list = []

        for i in range(0, len(food_id_list)):
            food_id = food_id_list[i]
            quantity = quantity_list[i]
            conversion_factor_id = conversion_factor_id_list[i]
            result_nb = Link_meal_food.objects.filter(meal_id=meal_id, food_id=food_id).count()
            if result_nb == 0:
                new_obj = Link_meal_food.objects.create(meal_id=meal_id, food_id=food_id, quantity=quantity,
                                                        food_name_scrapped=food_name_scrapped,
                                                        conversion_factor_id=conversion_factor_id)

                new_obj.save()
                new_link_meal_food_list.append(new_obj)

        return CreateLinkMealFoodList(linkMealFoodList=new_link_meal_food_list)

class CreateLinkMealFoodScrapping(graphene.Mutation):
    linkMealFood= graphene.List(LinkMealFoodType)

    class Arguments:
        meal_id = graphene.Int(required=True)
        food_text = graphene.String()
        quantity = graphene.Float()
        measure_name = graphene.String()
        meal_img_url = graphene.String()
        meal_name = graphene.String()

    def mutate(self, info, meal_id, food_text, quantity, meal_img_url, meal_name, measure_name=None):
        #1 get food
        food_text = food_text.strip().lower()
        meal_id_count = Meal.objects.filter(id=meal_id).count()
        if meal_id_count == 0:
            meal = Meal(id=meal_id, name=meal_name, imgUrl=meal_img_url)
            meal.save()

        best_score = -1
        food_id = None
        foodb = ""
        for elem in Food.objects.all():
            score = jellyfish.jaro_winkler_similarity(elem.name_fr.lower(), food_text)
            if score> 0.9 and score > best_score:
                food_id = elem.id
                foodb = elem.name_fr

        if food_id:
            print("similarity found with food in food table, foodtext : "+ food_text+"; fooddb : "+foodb)

        mapMarmittonFoods = MapMarmittonFood.objects.all()

        for elem in mapMarmittonFoods:
            score = jellyfish.jaro_winkler_similarity(elem.marmitton_food_name.lower(), food_text)
            if score> 0.9 and score > best_score:
                food_id = elem.food_id

        if food_id:
            food = Food.objects.get(id = food_id)
            print("similarity found with food in mapMarmittonFood, foodtext : "+ food_text+"; fooddb : "+food.name_fr)

        if not food_id:
            food_id =createMapMarmittonFood(food_text)

        lmf_hypothetic = Link_meal_food.objects.filter(food_id=food_id, meal_id=meal_id)
        if lmf_hypothetic.count() == 0:
            measure_id = getMeasureId(measure_name)
            conversion_factor_id = getConversionFactorId(food_id, measure_id)
            lmf = Link_meal_food(food_id=food_id, meal_id=meal_id, quantity=quantity,
                                 conversion_factor_id=conversion_factor_id)
            lmf.save()
            return lmf
        else:
            raise GraphQLError("This linkMealFood exist")




class ChangeMealFood(graphene.Mutation):
    changeLinkMealFoodInfo = graphene.Field(ChangeLinkMealFoodType)

    class Arguments:
        meal_id_target = graphene.Int(required=True)
        meal_id_origin = graphene.Int(required=True)
        food_id = graphene.Int(required=True)

    def mutate(self, info, meal_id_origin, meal_id_target, food_id):
        result_nb = Link_meal_food.objects.filter(meal_id=meal_id_origin, food_id=food_id).count()
        target_check_nb = Link_meal_food.objects.filter(meal_id=meal_id_target, food_id=food_id).count()

        if target_check_nb > 0:
            raise GraphQLError("Vous avez déjà ajouté cet aliment à ce repas")
        elif result_nb == 0:
            raise GraphQLError("There is no link meal food with this food id and meal id")
        elif result_nb == 1:
            linkMealFood = Link_meal_food.objects.get(food_id=food_id, meal_id=meal_id_origin)
            linkMealFood.meal_id = meal_id_target
            linkMealFood.save()

            changeLinkMealFoodInfo = ChangeLinkMealFoodType(old_meal_id=meal_id_origin, new_meal_id=meal_id_target,
                                                            food_id=food_id)

            return ChangeMealFood(changeLinkMealFoodInfo=changeLinkMealFoodInfo)


class UpdateLinkMealFood(graphene.Mutation):
    linkMealFood = graphene.Field(LinkMealFoodType)

    class Arguments:
        id = graphene.Int(required=True)
        quantity = graphene.Int(required=False)
        conversion_factor_id = graphene.Int(required=False)

    def mutate(self, info, id, quantity=None, conversion_factor_id=None):
        if Link_meal_food.objects.filter(id=id).count() > 0:
            linkMealFood = Link_meal_food.objects.get(id=id)
            linkMealFood.quantity = quantity
            linkMealFood.conversion_factor_id = conversion_factor_id
            linkMealFood.save()
            return UpdateLinkMealFood(linkMealFood=linkMealFood)
        else:
            raise GraphQLError("No object with this id")


class UpdateConsumptionHour(graphene.Mutation):
    linkMealRoutineProp = graphene.Field(LinkMealRoutinePropType)

    class Arguments:
        linkMealMealId = graphene.Int(required = True)
        newConsumptionHour = graphene.Float(required = True)

    def mutate(self, info, linkMealMealId, newConsumptionHour):
        lkRP = None
        if LinkMealRoutineProp.objects.filter(linkMealMeal_id = linkMealMealId).count()==0:
            lkRP = LinkMealRoutineProp.objects.create(linkMealMeal_id = linkMealMealId, consumption_hour=newConsumptionHour)
        else:
            lkRP = LinkMealRoutineProp.objects.get(linkMealMeal_id=linkMealMealId)
            lkRP.consumption_hour = newConsumptionHour
        lkRP.save()
        return UpdateConsumptionHour(linkMealRoutineProp = lkRP)





class DeleteLinkMealFood(graphene.Mutation):
    id_list = graphene.List(graphene.Int)

    class Arguments:
        linkMealFoodIdList = graphene.List(graphene.Int)

    def mutate(self, info, linkMealFoodIdList):
        link_meal_foods = Link_meal_food.objects.filter(id__in=linkMealFoodIdList)
        if link_meal_foods.count() < 1:
            raise GraphQLError("There is not link meal food with this id")
        else:
            id_list = []
            for link_meal_food in link_meal_foods:
                id_list.append(link_meal_food.id)
                link_meal_food.delete()

            return DeleteLinkMealFood(id_list=id_list)


class CreateLinkMealUser(graphene.Mutation):
    linkMealUser = graphene.Field(LinkMealUserType)

    class Arguments:
        meal_id = graphene.Int(required=True)

    def mutate(self, info, meal_id):
        user = info.context.user
        if not info.context.user.is_anonymous:
            link_meal_user = Link_meal_user(user_id=user.id, meal_id=meal_id)
            return CreateLinkMealUser(linkMealUser=link_meal_user)
        else:
            raise GraphQLError("not allowed")


class DeleteLinkMealUser(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        Link_meal_user.objects.get(id=id).delete()
        return DeleteLinkMealUser(id=id)


class DeleteMealList(graphene.Mutation):
    idList = graphene.List(graphene.Int)

    class Arguments:
        idList = graphene.List(graphene.Int)

    def mutate(self, info, idList):
        Meal.objects.filter(id__in=idList).delete()
        return DeleteMealList(idList=idList)


class DeleteSonMeal(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required = True)

    def mutate(self, info, id):
        LinkMealMeal.objects.get(id= id).delete()
        return DeleteSonMeal(id = id)


class Mutation(graphene.ObjectType):
    createLinkMealMeal= CreateLinkMealMeal.Field()
    create_link_meal_user = CreateLinkMealUser.Field()
    create_link_meal_food = CreateLinkMealFood.Field()
    create_meal = CreateMeal.Field()
    create_link_meal_food_scrapping = CreateLinkMealFoodScrapping.Field()
    update_meal = UpdateMeal.Field()
    CreateLinkMealFoodList = CreateLinkMealFoodList.Field()
    UpdateCustomMeal = UpdateCustomMeal.Field()
    DuplicateLinkRoutineMeal = DuplicateLinkRoutineMeal.Field()
    changeMealFood = ChangeMealFood.Field()
    updateLinkMealFood = UpdateLinkMealFood.Field()
    updateConsumptionHour = UpdateConsumptionHour.Field()
    create_scraping_meal = CreateScrapingMeal.Field()
    createCustomMeal = CreateCustomMeal.Field()
    delete_link_meal_user = DeleteLinkMealUser.Field()
    deleteLinkMealFood = DeleteLinkMealFood.Field()
    delete_meal_list = DeleteMealList.Field()
    delete_son_meal = DeleteSonMeal.Field()


def getFoodsFromSearch( food_text):
    createLMFQuery = """
        query($search:String!){
        foodsWithNutrientValue(search:$search, nutrientId:208){
            fId
            nameFr
            }
        }
        """
    url = 'http://localhost:9999/query'
    r = req.post(url, json={
        'query': createLMFQuery, 'variables':
            {
                "search": str(food_text),
                "nutrientId": 208
            }
    }
                 )
    print(r.status_code)
    foods = json.loads(r.text)['data']['foodsWithNutrientValue'][:50]
    return foods

def createMapMarmittonFood(food_text):
    print("choose an id for this food : " + food_text)
    foods = getFoodsFromSearch(food_text)
    for food in foods:
        print(str(food['fId']) + " : " + food['nameFr'])
    food_id = input("choose the right id bro")
    test = MapMarmittonFood(food_id=int(food_id), marmitton_food_name=food_text)
    test.save()
    return food_id


def isAlreadyInCsv(food_id, measure_name):
    already_in_csv = False
    with open(r'test.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            try:
                food_id_csv = row[0]
                measure_name_csv = row[2]
                if int(food_id_csv) == food_id and measure_name_csv.strip() == measure_name.strip():
                    return True
            except Exception:
                print("d")

    return already_in_csv

def writeInCsv(food_id,food_text,  isAlreadyInCs, measure_name):
    if not isAlreadyInCs:
        with open(r'test.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';')
            if not measure_name:
                measure_name = " "
            food_name = Food.objects.get(id = food_id).name_fr
            writer.writerow([food_name, food_text,  measure_name])


def getConversionFactorId(food_id, measure_id):
    conversion_factor_id = None
    conversion_factors = ConversionFactor.objects.filter(food_id=food_id, measure_id=measure_id)
    conversion_factors_size = len(conversion_factors)
    if conversion_factors_size == 0:
        conversion_factor = ConversionFactor(food_id=food_id, measure_id=measure_id, conversion_factor=0.5)
        conversion_factor.save()
    elif conversion_factors_size == 1:
        conversion_factor_id = conversion_factors[0].id
    elif conversion_factors_size > 0:
        raise GraphQLError("There is more than one conversion factor id for theses args")
    return conversion_factor_id


def getMeasureId(measure_name):
    measure_id = None
    if measure_name is None:
        measure_name = "-1"

    measures = Measure.objects.filter(nameFr=measure_name)
    if measures.count() == 1:
        measure_id = measures[0].id
    elif measures.count() == 0:
        measure = Measure(nameFr=measure_name)
        measure.save()
        measure_id = measure.id
    elif measures > 0:
        raise GraphQLError("There is more than Measure for this name")

    return measure_id