from .models import Product
from .serializer import ProductSerializer


def get_serializable_queryset(category_slug: str, product_slug: str = None) -> dict:
    if product_slug:
        product = Product.objects.filter(category__slug=category_slug).filter(slug=product_slug).first()
        serializer = ProductSerializer(instance=product)
    else:
        products = Product.objects.all().filter(category__slug=category_slug)
        serializer = ProductSerializer(instance=products, many=True)

    return serializer.data
