import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Cart


class CartItem(DjangoObjectType):
    class Meta:
        model = Cart


class AddToCartMutation(graphene.Mutation):
    class Arguments:
        productId = graphene.Int(required=True)
        quantity = graphene.Int(default_value=1)

    cart = graphene.List(CartItem)

    @login_required
    def mutate(self, info, productId, quantity):
        Cart.from_productId(info.context.user, productId, quantity)
        cartItems = info.context.user.cartItems.all()
        return AddToCartMutation(cart=cartItems)


class CartQuery:
    get_cart = graphene.List(CartItem)

    @login_required
    def resolve_get_cart(self, info):
        return info.context.user.cartItems.all()


class CartMutation:
    add_to_cart = AddToCartMutation.Field()
