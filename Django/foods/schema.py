import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from foods.utils import dice_coefficient
import base64


from foods.models import Food, FoodGroup, GoogleFoodsLabels, MapMarmittonFood, ConversionFactor, Measure, FoodImage
from nutrients.models import *


class FoodType(DjangoObjectType):
    class Meta:
        model = Food


class GroupType(DjangoObjectType):
    class Meta:
        model = FoodGroup


class GoogleFoodsLabelsType(DjangoObjectType):
    class Meta:
        model = GoogleFoodsLabels


class MapMarmittonFoodType(DjangoObjectType):
    class Meta:
        model = MapMarmittonFood


class ConversionFactorType(DjangoObjectType):
    class Meta:
        model = ConversionFactor


class MeasureType(DjangoObjectType):
    class Meta:
        model = Measure

class FoodGroupType(DjangoObjectType):
 class Meta:
     model = FoodGroup


def destroy_plurials(text):
    text_splitted = text.split(" ")
    new_text_recomposed = ""
    for text in text_splitted:
        if text[len(text) - 1] == 's':
            text = text[:len(text) - 1]
        new_text_recomposed += text + " "
    return new_text_recomposed


class Query(object):
    food = graphene.Field(FoodType, id=graphene.Int(required=True))
    foods = graphene.List(FoodType, search=graphene.String(), admin=graphene.Boolean())
    topFoodsByNutrient = graphene.List(FoodType, nutrientId=graphene.Int())
    foodGroups = graphene.List(GroupType)
    googleFoodLabelsByFood = graphene.List(GoogleFoodsLabelsType, food_id=graphene.Int(required=True))
    mapMarmittonFood = graphene.List(MapMarmittonFoodType, marmitton_food_name=graphene.String(required=True))
    conversionFactorList = graphene.List(ConversionFactorType, food_id=graphene.Int(required=True))
    foodGroups = graphene.List(FoodGroupType)
    giveDefaultConversionFactorToFoods = graphene.List(graphene.Int)

    def resolve_foodImage(self, info):
        return FoodImage.objects.all()


    def resolve_foodGroups(self, info):


        return FoodGroup.objects.all()

    def resolve_giveDefaultConversionFactorToFoods(self, info):
        foods = Food.objects.all()
        food_id_list =[]
        for food in foods:
            food_id = food.id
            result = ConversionFactor.objects.filter(food_id=food_id)
            if result.count() < 1:
                ConversionFactor(food_id=food_id, conversion_factor=0.01, measure_id=1578).save()
                ConversionFactor(food_id=food_id, conversion_factor=1, measure_id=1455).save()
                food_id_list.append(food_id)

        return food_id_list

    def resolve_conversionFactorList(self, info, food_id):


        result = ConversionFactor.objects.filter(food_id=food_id)
        if result.count() < 1:
            ConversionFactor(food_id=food_id, conversion_factor=0.01, measure_id=1578).save()
            ConversionFactor(food_id=food_id, conversion_factor=1, measure_id=1455).save()

        return ConversionFactor.objects.filter(food_id=food_id)

    def resolve_topFoodsByNutrient(self, info, nutrientId):
        top_link_nutrient_foods = LinkNutrientFood.objects.filter(nutrient_id=nutrientId,
                                                                  food__activated=True).order_by('-value')[0:200]
        food_id_list = []
        food_list = []
        for elem in top_link_nutrient_foods:
            food_id_list.append(elem.food_id)
            food = Food.objects.filter(id=elem.food_id)[0]
            food_list.append(food)

        return food_list

    def resolve_foods(self, info, search=None, admin=False):
        foods = Food.objects.all()
        if not admin:
            foods = foods.filter(activated=True)

        # default
        if not search:
            result = foods
            result = result[:25]
        else:

            import unidecode

            search = unidecode.unidecode(search)
            score_list = []
            result = []


            total_time = 0
            for food in foods:
                score = dice_coefficient(search, food.name_fr)
                score_list.append({"food": food, "score": score})
            print(total_time, "seconds")


            def sort_score_obj(e):
                return -e["score"]

            score_list.sort(key=sort_score_obj)
            score_list = score_list[:25]
            for score_obj in score_list:
                result.append(score_obj['food'])

        return result

    def resolve_mapMarmittonFood(self, info, marmitton_food_name):
        result = MapMarmittonFood.objects.filter(marmitton_food_name=marmitton_food_name)
        text = destroy_plurials(marmitton_food_name)
        if result.count() < 1:
            marmitton_foods_names = MapMarmittonFood.objects.all()
            for elem in marmitton_foods_names:
                elem_text = elem.marmitton_food_name
                elem_text = destroy_plurials(elem_text)
                if elem_text == text:
                    result = MapMarmittonFood.objects.filter(marmitton_food_name=elem.marmitton_food_name)
                    marmitton_food_name = text

        if result.count() == 1:
            toIncrement = MapMarmittonFood.objects.get(marmitton_food_name=marmitton_food_name)
            toIncrement.recurrence += 1
            toIncrement.save()

        return result

    def resolve_googleFoodLabelsByFood(self, info, food_id):
        return GoogleFoodsLabels.objects.filter(food_id=food_id)

    def resolve_food(self, info, id):

        return Food.objects.get(id=id)

    def resolve_foodGroups(self, info):
        return FoodGroup.objects.all()


class CreateDefaultPortionMutation(graphene.Mutation):
    nb_created = graphene.Int()

    def mutate(self, info):
        nb_created = 0
        foods = Food.objects.all()
        default_measure_conv_factor_list = [{"measure_id": 1455, "conversion_factor": 1},
                                            {"measure_id": 1578, "conversion_factor": 0.01}]
        for food in foods:
            for default_meas_conv in default_measure_conv_factor_list:
                measure_id = default_meas_conv["measure_id"]
                conversion_factor = default_meas_conv["conversion_factor"]
                if ConversionFactor.objects.filter(measure_id=measure_id, food_id=food.id).count() < 1:
                    ConversionFactor(food_id=food.id, measure_id=measure_id, conversion_factor=conversion_factor).save()
                    nb_created += 1
                    print(nb_created)
                else:
                    print("default measure already existing for this food")

        return CreateDefaultPortionMutation(nb_created=nb_created)


class CreateFoodGroup(graphene.Mutation):
    foodGroup = graphene.Field(GroupType)

    class Arguments:
        id = graphene.Int()
        name_en = graphene.String(required=True)
        name_fr = graphene.String(required=True)

    def mutate(self, info, id, name_en, name_fr):
        if FoodGroup.objects.filter(id=id).count():
            foodGroup = FoodGroup.objects.get(id=id)
            foodGroup.name_en = name_en
            foodGroup.name_fr = name_fr
        else:
            foodGroup = FoodGroup(id=id, name_en=name_en, name_fr=name_fr)
            foodGroup.save()
        return CreateFoodGroup(foodGroup=foodGroup)


class CreateMapMarmittonFood(graphene.Mutation):
    mapMarmittonFood = graphene.Field(MapMarmittonFoodType)

    class Arguments:
        id = graphene.Int()
        food_id = graphene.Int()
        marmitton_food_name = graphene.String(required=True)
        negligable = graphene.Boolean()

    def mutate(self, info, marmitton_food_name, negligable=False, food_id=None):
        mapMarmittonFood = MapMarmittonFood.objects.create(food_id=food_id, marmitton_food_name=marmitton_food_name,
                                                           negligable=negligable)
        mapMarmittonFood.save()
        return CreateMapMarmittonFood(mapMarmittonFood=mapMarmittonFood)


class CreateGoogleFoodsLabels(graphene.Mutation):
    googleFoodsLabels = graphene.Field(GoogleFoodsLabelsType)

    class Arguments:
        food_id = graphene.Int()
        img_url = graphene.String()
        label = graphene.String()

    def mutate(self, info, food_id, img_url, label):
        new_obj = GoogleFoodsLabels(food_id=food_id, img_url=img_url, label=label)
        new_obj.save()
        return CreateGoogleFoodsLabels(googleFoodsLabels=new_obj)



class CreateFood(graphene.Mutation):
    food = graphene.Field(FoodType)

    class Arguments:
        id = graphene.Int()
        name_en = graphene.String()
        name_fr = graphene.String()

    def mutate(self, info, id, name_en=None, name_fr=None):
        if Food.objects.filter(id=id).count():
            food = Food.objects.get(id=id)
            food.name_en = name_en
            food.name_fr = name_fr
            food.save()
        else:
            food = Food(id=id, name_en=name_en, name_fr=name_fr)
            food.save()
        return CreateFood(food=food)




# class CreateFoodImage(graphene.Mutation):
#     foodImage = graphene.Field(FoodType)
#
#     class Arguments:
#         foodId = graphene.Int()
#         image = graphene.String()
#     def mutate(self, info, foodId, image):
#
#         img_to_save_in_db = base64.b64encode(image)
#
#
#         test = GetNpArrayImgFromByteStr(img_to_save_in_db)
#         food_id_number = Food.objects.filter(id = foodId).count()
#         if food_id_number == 0:
#             test = FoodImage(food_id = foodId, image=img_to_save_in_db)
#             test.save()
#
#         return CreateFoodImage(foodImage = test)





class ClickFood(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        food = Food.objects.get(id = id)
        food.nb_of_selection += 1
        food.save()
        return ClickFood(id=id)



class ToggleActivationFood(graphene.Mutation):
    food = graphene.Field(FoodType)

    class Arguments:
        id = graphene.Int()
        activated = graphene.Boolean()

    def mutate(self, info, id, activated):
        if Food.objects.filter(id=id).count() == 0:
            raise GraphQLError("There is no food with this Id")
        elif Food.objects.filter(id=id).count() == 1:
            food_to_update = Food.objects.get(id=id)
            food_to_update.activated = activated
            food_to_update.save()
            return ToggleActivationFood(food=food_to_update)
        else:
            raise GraphQLError("Toogle Activate Food error")


class CreateCliqualConversionFactor(graphene.Mutation):
    resultList = graphene.List(ConversionFactorType)

    class Arguments:
        canada_food_id = graphene.Int()
        cliqual_food_id = graphene.Int()

    def mutate(self, info, canada_food_id, cliqual_food_id):
        resultList = []
        conversionFactorList = ConversionFactor.objects.filter(food_id=canada_food_id)

        if conversionFactorList.count() > 0:
            for convFac in conversionFactorList:
                if ConversionFactor.objects.filter(food_id=cliqual_food_id, measure_id=convFac.measure_id).count() < 1:
                    newConvFactor = ConversionFactor(food_id=cliqual_food_id, measure_id=convFac.measure_id,
                                                     conversion_factor=convFac.conversion_factor)
                    newConvFactor.save()
                    resultList.append(newConvFactor)
                else:
                    raise GraphQLError("There is already a conversion factor for this cliqual food id and measure id")

        else:
            raise GraphQLError("No conversion Factor for this canadian food id")

        return CreateCliqualConversionFactor(resultList=resultList)


class UpdateFood(graphene.Mutation):
    food = graphene.Field(FoodType)

    class Arguments:
        id = graphene.Int(required=True)
        name_en = graphene.String()

    def mutate(self, info, id, name_en):
        food = Food.objects.get(id=id)
        if name_en:
            food.name_en = name_en

        food.save()

        return UpdateFood(food=food)


class DeleteFood(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        food = Food.objects.get(id=id)
        food.delete()

        return DeleteFood(id=id)


class Mutation(graphene.ObjectType):
    click_food = ClickFood.Field()
    create_food = CreateFood.Field()
    update_food = UpdateFood.Field()
    delete_food = DeleteFood.Field()
    createGoogleFoodsLabels = CreateGoogleFoodsLabels.Field()
    createCliqualConversionFactor = CreateCliqualConversionFactor.Field()
    CreateFoodGroup = CreateFoodGroup.Field()
    create_map_marmitton_food = CreateMapMarmittonFood.Field()
    createDefaultPortion = CreateDefaultPortionMutation.Field()
    toggleActivationFood = ToggleActivationFood.Field()
    # createFoodImage = CreateFoodImage.Field()
