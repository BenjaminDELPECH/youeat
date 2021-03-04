import graphene
import graphql_jwt


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user_id = graphene.Int()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user_id=info.context.user.id)