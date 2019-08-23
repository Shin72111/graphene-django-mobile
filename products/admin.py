from django.contrib import admin
from .models import Supplier, Product, ProductImage

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(ProductImage)
