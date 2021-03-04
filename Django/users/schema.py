import graphene
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.utils.encoding import force_bytes, force_text

from django.core.mail import send_mail
from utils.sendPostMutation import sendPostMutation
from graphene_django.utils.testing import GraphQLTestCase

from graphql_jwt.testcases import JSONWebTokenTestCase
from foods.models import ConversionFactor
from users.models import Profile
from utils.User import getUserId
import os
import random

from meal.models import Meal, LinkMealMeal, Link_meal_food
import json
from django.conf import settings

import requests as req

from utils.api import getDjangoApiUrl

obtainToken = '''
            mutation($username : String!, $password: String!){
                tokenAuth(username:$username, password:$password){
                    userId
                    token
                }
            }
            '''

graphqlJwtTokenQuery = """mutation TokenAuth($username: String!, $password: String!) {
                  tokenAuth(username: $username, password: $password) {
                    token
                    payload
                    refreshExpiresIn
                  }
                }"""


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    user_google_connexion = graphene.Field(UserType, id=graphene.Int(required=True),
                                           username=graphene.String(required=True),
                                           email=graphene.String(), password=graphene.String(required=True))

    profile = graphene.Field(ProfileType)

    is_staff = graphene.Field(graphene.Boolean)

    def resolve_user(self, info):
        userId = getUserId(info.context)
        if userId == -1:
            raise GraphQLError("user not authenticated")
        else:
            return User.objects.get(id=userId)

    def resolve_profile(self, info):
        user_id = getUserId(info.context)

        if user_id == -1:
            raise GraphQLError("This user doesnt exist, user id : " + str(user_id))
        profiles = Profile.objects.filter(user_id=user_id)
        if profiles.count() == 0:
            profil = Profile(age=35, poid=70, taille=175, activity=1.375, sexe=1, user_id=user_id)
            profil.save()
        elif profiles.count() > 1:
            for profil in profiles:
                profil.delete()

        return Profile.objects.get(user_id=user_id)

    def resolve_is_admin(self, info):
        user = info.context.user
        return user.is_staff

    def resolve_user_google_connexion(self, info, id, username, email, password):
        if User.objects.filter(id=id).count() == 0:
            user = User.objects.create_user(id=id, username=username,
                                            password=password)
            user.set_password(password)
            if email:
                user.email = email
            user.save()
        else:
            user = User.objects.get(id=id)

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        isSocialAccount = graphene.Boolean(required=False)
        anonymousUserId = graphene.Int(required=False)

    def mutate(self, info, email, password, isSocialAccount=False, anonymousUserId=-1):
        code = 0
        if User.objects.filter(username=email).count() > 0 or User.objects.filter(email=email).count() > 0:
            code = 1

        if code == 1:
            user = User.objects.get(username=email)
            print(user)
            # an user is already using this email adress
            profile = Profile.objects.get(user_id=user.id)
            # if not profile.social_account:
            #     raise GraphQLError("no_social_account_already_exist")
            if not isSocialAccount:
                raise GraphQLError("Cette adresse mail est déjà relié à un compte")
            elif not profile.social_account and isSocialAccount:
                raise GraphQLError("google_accont_with_same_email_adress_exist")
            else:
                raise GraphQLError("unknow error")

        else:
            if anonymousUserId > 0:
                user = User(id=anonymousUserId, username=email, email=email, password=password)
                user.set_password(password)
                user.save()
            else:
                try:
                    user = User(username=email, email=email, password=password)
                    user.set_password(password)
                    user.save()
                    variables = {
                        'username': user.email,
                        'password': password
                    }
                    from secrets import token_urlsafe
                    activation_token = token_urlsafe(16)

                    user.is_active = False
                    user.save()
                    profile = Profile.objects.create(user_id=user.id, social_account=isSocialAccount,
                                                     activation_token=activation_token)
                    profile.save()
                    mail_subject = "Activate your account"

                    user.is_active = True
                    user.save()

                    token = getToken(password, user)

                    user.is_active = False
                    user.save()
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': info.context.headers['origin'],
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'activation_token': activation_token,
                        'token': token
                    })
                    from_mail = str('from@' + settings.EMAIL_HOST),
                    recipient_list = []
                    recipient_list.append(email)

                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email="no_reply@youeat.fr",
                        recipient_list=recipient_list,
                        fail_silently=False,
                    )
                except:
                    user.delete()
                    pass

            ## create default mealse
            meal1 = Meal.objects.create(name="Petit-déjeuner exemple", author=user, object_type_id=2)
            meal1.save()

            #
            # new_obj = Link_meal_food.objects.create(meal_id=meal_id, food_id=food_id, quantity=quantity,
            #                                         food_name_scrapped=food_name_scrapped,
            # #                                         conversion_factor=conversion_factor_set)
            # new_obj.save()

            food1_id = 129
            conversion_factor = ConversionFactor.objects.filter(food_id=food1_id).first()
            lmf1 = Link_meal_food.objects.create(meal=meal1, food_id=food1_id, conversion_factor=conversion_factor,
                                                 quantity=1)
            lmf1.save()

            food2_id = 1704
            conversion_factor = ConversionFactor.objects.filter(food_id=food2_id).first()
            Link_meal_food.objects.create(meal=meal1, food_id=food2_id, conversion_factor=conversion_factor,
                                          quantity=1).save()

            routine1 = Meal.objects.create(name="Routine 1 exemple", author=user, object_type_id=1)
            routine1.save()

            new_link = LinkMealMeal.objects.create(mom_meal_id=routine1.id, son_meal_id=meal1.id)
            new_link.save()

            return CreateUser(user=user)


def getToken(password, user):
    variables = {"username": user.username, "password": password}
    url = getDjangoApiUrl()
    test = sendPostMutation(url, obtainToken, variables)
    tokenAuthResp = test['data']['tokenAuth']
    token = tokenAuthResp['token']
    return token

from django.contrib.auth import get_user_model


class ActivateUser(graphene.Mutation):
    userId = graphene.Int()

    class Arguments:
        activationToken = graphene.String()

    def mutate(self, info, activationToken):

        try:
            profile = Profile.objects.get(activation_token=activationToken)
            user_id = profile.user_id
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                return ActivateUser(userId=user.id)
            except:
                raise GraphQLError("unknow error")
        except:
            raise GraphQLError("unknow error")


class SendVerificationCodeMail(graphene.Mutation):
    mail_sended = graphene.Boolean()

    class Arguments:
        email = graphene.String()

    def mutate(self, info, email):
        try:
            verification_code = random.randint(10000, 999999)

            user = User.objects.get(email=email)

            subject = "{} est votre code de récupération de compte youeat.fr".format(verification_code)
            profile = Profile.objects.get(user_id=user.id)
            profile.activation_code_forget_password = verification_code
            profile.save()
            recipient_list = []
            recipient_list.append(user.username)
            send_mail(subject=subject,
                      message=subject,
                      from_email="no_reply@youeat.fr",
                      recipient_list=recipient_list,
                      fail_silently=False)
            return SendVerificationCodeMail(mail_sended=True)
        except:
            raise GraphQLError("unknow error")


class VerifyCode(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        code = graphene.Int()
        email = graphene.String()

    def mutate(self, info, code, email):
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user_id=user.id)
            if profile.activation_code_forget_password == code:
                return VerifyCode(success=True)
            else:
                raise GraphQLError("wrong code")
        except:
            raise GraphQLError("unknow error")

class ChangePassword(graphene.Mutation):
    token = graphene.String()
    userId = graphene.Int()

    class Arguments:
        email = graphene.String()
        newPassword = graphene.String()

    def mutate(self, info, email, newPassword):
        try:
            user = User.objects.get(email=email)
            user.set_password(newPassword)
            user.save()
            token = getToken(newPassword, user)
            return ChangePassword(token = token, userId = user.id)
        except:
            raise GraphQLError("unknow error")


class UpdateProfile(graphene.Mutation):
    updateProfile = graphene.Field(ProfileType)

    class Arguments:
        sexe = graphene.Int()
        age = graphene.Int()
        poid = graphene.Int()
        taille = graphene.Int()
        activity = graphene.Float()

    def mutate(self, info, age, poid, taille, activity, sexe):
        user_id = getUserId(info.context)
        if Profile.objects.filter(user_id=user_id).count() > 0:
            profil = Profile.objects.get(user_id=user_id)
            profil.age = age
            profil.poid = poid
            profil.taille = taille
            profil.activity = activity
            profil.sexe = sexe

            profil.save()
        else:
            profil = Profile(age=age, poid=poid, taille=taille, activity=activity, sexe=sexe, user_id=user_id)
            profil.save()
        return UpdateProfile(updateProfile=profil)


class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        user_id = graphene.Int()

    def mutate(self, info, user_id):
        success = False
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            success = True
        except:
            pass
        return DeleteUser(success=success)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()
    delete_user = DeleteUser.Field()
    activate_user = ActivateUser.Field()
    sendVerificationCodeMail = SendVerificationCodeMail.Field()
    verifyCode = VerifyCode.Field()
    changePassword = ChangePassword.Field()
