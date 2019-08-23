import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import staff_member_required

from .models import Supplier, Product, ProductImage


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        exclude = ('cart_set', 'orderitem_set')


class ProductQuery(object):
    get_supplier = graphene.Field(SupplierType,
                                  name=graphene.String())
    get_suppliers = graphene.List(SupplierType)

    get_product = graphene.Field(ProductType,
                                 name=graphene.String(), id=graphene.Int())
    get_products = graphene.List(ProductType)

    image = graphene.Field(ProductImageType)

    def resolve_get_supplier(self, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return Supplier.objects.get(name=name)
        return None

    def resolve_get_product(self, info, **kwargs):
        id = kwargs.get('name')
        name = kwargs.get('name')
        if id is not None:
            return Product.objects.get(pk=id)
        if name is not None:
            return Product.objects.get(name=name)
        return None

    def resolve_get_suppliers(self, info, **kwargs):
        return Supplier.objects.all()

    def resolve_get_products(self, info, **kwargs):
        return Product.objects.all()


class AddSupplierMutation(graphene.Mutation):
    supplier = graphene.Field(SupplierType)

    class Arguments:
        name = graphene.String(required=True)

    @staff_member_required
    def mutate(self, info, name):
        supplier = Supplier.objects.create(name=name)
        return AddSupplierMutation(supplier=supplier)


class AddProductMutation(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        supplier = graphene.String(required=True)
        name = graphene.String(required=True)
        productInfo = graphene.String(required=True)
        price = graphene.Float(required=True)

    @staff_member_required
    def mutate(self, info, supplier, name, productInfo, price):
        supplier = Supplier.objects.get(name=supplier)
        if supplier is None:
            raise Exception('Supplier does not exist')
        product = Product.objects.create(name=name, info=productInfo,
                                         supplier=supplier, price=price)
        return AddProductMutation(product=product)


class ProductMutation:
    add_supplier = AddSupplierMutation.Field()
    add_product = AddProductMutation.Field()
