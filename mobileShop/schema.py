import graphene
import graphql_jwt

from users.schema import UserMutation
from cart.schema import CartMutation, CartQuery
from orders.schema import OrderMutation, OrderQuery
from products.schema import ProductQuery, ProductMutation


class Query(ProductQuery, CartQuery, OrderQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType, UserMutation,
               CartMutation, OrderMutation, ProductMutation):
    login = graphql_jwt.ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
