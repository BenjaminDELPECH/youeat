import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)