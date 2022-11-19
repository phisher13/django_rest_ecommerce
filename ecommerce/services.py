import requests
from django.core.cache import cache

from .models import (
    Product,
    Favourite,
    Cart,
    Order
)
from .serializer import (
    ProductSerializer,
    FavouritesCreateSerializer,
    CartSerializer,
    OrderSerializer
)


def get_all_products(request: requests) -> dict:
    category = request.GET['category']
    if cache.get(category):
        products = cache.get(category)
    else:
        products = Product.objects.all().filter(category__name=category)
        cache.set(category, products)
    serializer = ProductSerializer(instance=products, many=True)

    return serializer.data


def get_detail_product(slug: str) -> dict:
    if cache.get(slug):
        product = cache.get(slug)
    else:
        product = Product.objects.filter(slug=slug).first()
        cache.set(slug, product)
    serializer = ProductSerializer(instance=product)

    return serializer.data


def add_products_to_favourite(request: requests) -> dict:
    user = request.user
    favourite = Favourite.objects.filter(user=user).first()
    if favourite:
        favourite.products.add(request.data['product'])
    else:
        favourite = Favourite.objects.create(
            user=user
        )
        favourite.products.add(request.data['product'])
    serializer = FavouritesCreateSerializer(instance=favourite)
    return serializer.data


def add_products_to_cart(request) -> dict:
    user = request.user
    cart = Cart.objects.filter(product_id=request.data['product_id']).filter(user=user).first()
    if cart:
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart.objects.create(
            quantity=1,
            product_id=request.data['product_id'],
            user=user
        )

    serializer = CartSerializer(instance=cart)
    return serializer.data


def crete_new_order(request) -> dict:
    user = request.user
    order = Order.objects.create(
        user=user,
        cart_id=request.data['cart_id']
    )
    serializer = OrderSerializer(instance=order)

    return serializer.data
