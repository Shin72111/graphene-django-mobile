from django.db import models

from orders.models import Order
from products.models import Product


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    @classmethod
    def from_cart(cls, order):
        cartItems = order.owner.cartItems.all()
        orderItems = []
        for item in cartItems:
            if item.quantity > 0:
                orderItems.append(OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                ))
            item.delete()
        return orderItems
