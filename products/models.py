from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()
    price = models.FloatField()
    supplier = models.ForeignKey(
        Supplier, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return f'<Product {self.product.name} image>'
