from .models import Product, Favourite, Cart
from .serializer import ProductSerializer, FavouritesCreateSerializer, CartSerializer


def get_serializable_queryset(category_slug: str, product_slug: str = None) -> dict:
    if product_slug:
        product = Product.objects.filter(category__slug=category_slug).filter(slug=product_slug).first()
        serializer = ProductSerializer(instance=product)
    else:
        products = Product.objects.all().filter(category__slug=category_slug)
        serializer = ProductSerializer(instance=products, many=True)

    return serializer.data


def add_products_to_favourite(request):
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


def add_products_to_cart(request):
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
