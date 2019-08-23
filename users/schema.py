import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.utils import jwt_encode, jwt_payload


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'is_staff')

    token = graphene.String()

    def resolve_token(self, info):
        payload = jwt_payload(self)
        return jwt_encode(payload)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class UserMutation():
    create_user = CreateUser.Field()
