from django.db import models
from django.shortcuts import get_object_or_404

from users.models import User
from products.models import Product


class Cart(models.Model):
    owner = models.ForeignKey(
        User, related_name='cartItems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('owner', 'product')

    @classmethod
    def from_productId(cls, user, productId, quantity):
        if quantity < 0:
            raise Exception('Invalid quantity')
        product = get_object_or_404(Product, id=productId)
        cart = user.cartItems.filter(product=product).first()
        if cart is not None:
            cart.quantity = quantity
            cart.save()
            return cart
        return Cart.objects.create(
            owner=user, product=product, quantity=quantity)
