import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from meal.models import Meal
from routine.models import RoutineList, Routine, Link_routine_meal

NOT_ALLOWED = "not allowed"


class RoutineType(DjangoObjectType):
    class Meta:
        model = Routine


class RoutineListType(DjangoObjectType):
    class Meta:
        model = RoutineList


class LinkRoutineMealType(DjangoObjectType):
    class Meta:
        model = Link_routine_meal


class Query(object):
    routine = graphene.Field(RoutineType, id=graphene.Int())
    routines = graphene.List(RoutineType)
    routineList = graphene.List(RoutineListType)
    link_routine_meal = graphene.List(LinkRoutineMealType, routine_id=graphene.Int())

    def resolve_routines(self, info):
        return Routine.objects.all()

    def resolve_link_routine_meal(self, info, routine_id):
        user = info.context.user
        if not user.is_anonymous:
            links = Link_routine_meal.objects.filter(routine_id=routine_id)
            return links.distinct()
        else:
            raise GraphQLError(NOT_ALLOWED)

    def resolve_routine(self, info, id):
        if Routine.objects.filter(id=id).count() > 0:
            return Routine.objects.get(id=id)
        else:
            raise GraphQLError(message="Pas de routine correspondante")

    def resolve_routineList(self, info):
        user = info.context.user
        if not user.is_anonymous:
            links = RoutineList.objects.filter(user_id=user.id).order_by('-routine__last_updated')
            return links.distinct()
        else:
            raise GraphQLError("*TEST TEST")


class CreateRoutine(graphene.Mutation):
    routineListElem = graphene.Field(RoutineListType)

    class Arguments:
        name = graphene.String(required=False)

    def mutate(self, info, name="New routine"):
        user = info.context.user
        user_id = -1
        if user_id in info.context.COOKIES:
            user_id = info.context.COOKIES["user_id"]
        if user_id != -1:
            routine = Routine(name=name, author_id=user.id)
            routine.save()
            routine_list_elem = RoutineList(user_id=user.id, routine_id=routine.id)
            routine_list_elem.save()
            return CreateRoutine(routineListElem=routine_list_elem)
        else:
            raise GraphQLError(NOT_ALLOWED)


class CreateCustomRoutine(graphene.Mutation):
    routineElem = graphene.Field(RoutineType)

    class Arguments:
        name = graphene.String(required=False)
        repasNumber = graphene.Int()

    def mutate(self, info, name, repasNumber=None):
        user_id = info.context.user.id

        routine = Routine(name=name, author_id=user_id)
        routine.save()
        consumption_hour_default_list = [9, 12, 18]
        for i in range(repasNumber):
            createCustomMeal = Meal(name="Repas" + str(i))
            createCustomMeal.save()
            consumption_hour_default_val = consumption_hour_default_list[i]
            newLinkRoutineMeal = Link_routine_meal(routine=routine, meal=createCustomMeal, consumption_hour=consumption_hour_default_val)
            newLinkRoutineMeal.save()

        return CreateCustomRoutine(routineElem=routine)


class DeleteCustomRoutine(graphene.Mutation):
    routineId = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):

        if Link_routine_meal.objects.filter(routine_id=id).count() > 0:
            linkRoutineMealList = Link_routine_meal.objects.filter(routine_id=id)
            for elem in linkRoutineMealList:
                elem.delete()

        if Routine.objects.filter(id=id).count() > 0:
            Routine.objects.get(id=id).delete()

        return DeleteCustomRoutine(routineId=id)


class UpdateTitleRoutine(graphene.Mutation):
    routineListElem = graphene.Field(RoutineListType)

    class Arguments:
        routine_id = graphene.Int(required=True)
        title = graphene.String()

    def mutate(self, info, routine_id, title):
        user = info.context.user
        if not user.is_anonymous:
            routine = Routine.objects.get(id=routine_id)
            routine.name = title
            routine.save()
            routineListElem = RoutineList.objects.get(routine_id=routine_id)
            return UpdateTitleRoutine(routineListElem=routineListElem)

        else:
            raise GraphQLError(NOT_ALLOWED)


####################Link Routine Meal##############################
class CreateLinkRoutineMeal(graphene.Mutation):
    linkRoutineMeal = graphene.Field(LinkRoutineMealType)

    class Arguments:
        meal_id = graphene.Int(required=True)
        routine_id = graphene.Int(required=True)


    def mutate(self, info, meal_id, routine_id):
        user = info.context.user
        if not user.is_anonymous:
            linkRoutineMeal = Link_routine_meal(routine_id=routine_id, meal_id=meal_id, consumption_hour=12)
            linkRoutineMeal.save()
            return CreateLinkRoutineMeal(linkRoutineMeal=linkRoutineMeal)
        else:
            raise GraphQLError(NOT_ALLOWED)


class UpdateLinkRoutineMeal(graphene.Mutation):
    linkRoutineMeal = graphene.Field(LinkRoutineMealType)

    class Arguments:
        mealId = graphene.Int(required=True)
        routineId = graphene.Int(required=True)
        consumptionHour = graphene.Int(required=False)

    def mutate(self, info, mealId, routineId, consumptionHour):
        user = info.context.user
        if not user.is_anonymous:
            linkRoutineMeal = Link_routine_meal.objects.filter(routine_id=routineId, meal_id=mealId)
            if linkRoutineMeal.count() == 1:
                linkRoutineMeal = Link_routine_meal.objects.get(routine_id=routineId, meal_id=mealId)
                if consumptionHour:
                    linkRoutineMeal.consumption_hour = consumptionHour

                else:
                    raise GraphQLError("No update to do")

                linkRoutineMeal.save()

            else:
                raise GraphQLError("No Object with this routine id or meal id")

            return UpdateLinkRoutineMeal(linkRoutineMeal=linkRoutineMeal)

        else:
            raise GraphQLError(NOT_ALLOWED)


class DeleteLinkRoutineMeal(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        routineId = graphene.Int(required=True)
        mealId = graphene.Int(required=True)

    def mutate(self, info, routineId, mealId):
        if Link_routine_meal.objects.filter(routine_id=routineId).count() < 1:
            raise GraphQLError("There is not linkRoutineMeal with this routine Id")
        else:
            links = Link_routine_meal.objects.filter(routine_id=routineId)
            if links.filter(meal_id=mealId).count() < 1:
                raise GraphQLError("There is not linkRoutineMeal with this routine id and meal id")
            else:
                link = links.get(routine_id=routineId, meal_id=mealId)
                graphene.Int
                linkIdDeleted = link.id
                link.delete()
                return DeleteLinkRoutineMeal(id=linkIdDeleted)


####################Link Routine Meal##############################

class DeleteRoutine(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        Routine.objects.get(id=id).delete()
        return DeleteRoutine(id=id)


class Mutation(graphene.ObjectType):
    create_routine = CreateRoutine.Field()
    create_custom_routine = CreateCustomRoutine.Field()
    delete_routine = DeleteRoutine.Field()

    create_link_routine_meal = CreateLinkRoutineMeal.Field()
    UpdateLinkRoutineMeal = UpdateLinkRoutineMeal.Field()
    delete_link_routine_meal = DeleteLinkRoutineMeal.Field()

    delete_custom_routine = DeleteCustomRoutine.Field()
    update_title_routine = UpdateTitleRoutine.Field()
