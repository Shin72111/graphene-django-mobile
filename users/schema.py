import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql_jwt.decorators import superuser_required
from django.shortcuts import get_object_or_404


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


class NominateStaffMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        userId = graphene.Int()

    @superuser_required
    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        userId = kwargs.get('userId')

        if userId:
            user = get_object_or_404(get_user_model(), id=userId)
        elif username:
            user = get_object_or_404(get_user_model(), username=username)
        else:
            raise Exception('Username or user id is required to nominate')
        user.is_staff = True
        user.save()

        return NominateStaffMutation(user=user)


class UserMutation():
    create_user = CreateUser.Field()
    nominate_staff = NominateStaffMutation.Field()
