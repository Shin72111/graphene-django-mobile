import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Order
from orderItems.models import OrderItem


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        exclude = ('order',)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class MakeOrderMutation(graphene.Mutation):
    order = graphene.Field(OrderType)

    @login_required
    def mutate(self, info):
        user = info.context.user
        count = 0
        for item in user.cartItems.all():
            count += item.quantity
        if count == 0:
            raise Exception('No item in cart to order')

        order = Order.objects.create(owner=user)
        OrderItem.from_cart(order)
        return MakeOrderMutation(order=order)


class OrderMutation:
    make_order = MakeOrderMutation.Field()


class OrderQuery:
    get_orders = graphene.List(OrderType)
    get_order = graphene.Field(OrderType, id=graphene.Int(required=True))

    @login_required
    def resolve_get_orders(self, info):
        return info.context.user.orders.all()

    @login_required
    def resolve_get_order(self, info, id):
        return info.context.user.orders.filter(pk=id).first()
