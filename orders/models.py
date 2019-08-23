from django.db import models

from users.models import User


class Order(models.Model):
    owner = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
