import http

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView, Response

from .models import Category, Product, Favourite, Cart, Order
from .serializer import (
    CategorySerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CategoryCreateSerializer,
    FavouritesSerializer,
    CartSerializer, OrderSerializer,
)
from .services import get_serializable_queryset, add_products_to_favourite, add_products_to_cart, crete_new_order
from .permissions import IsOwner


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductApiView(APIView):
    def get(self):
        category_slug = self.request.GET.get('category')
        product_slug = self.request.GET.get('product', None)
        data = get_serializable_queryset(category_slug=category_slug, product_slug=product_slug)
        return Response(status=http.HTTPStatus.OK, data=data)


class CategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class FavouriteView(DestroyAPIView):
    lookup_field = 'uuid'
    serializer_class = FavouritesSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Favourite.objects.all().filter(user=user)


class FavouriteListView(ListAPIView):
    serializer_class = FavouritesSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Favourite.objects.all().filter(user=user)


class FavouriteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = add_products_to_favourite(self.request)
        return Response(status=201, data=data)


class CartView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = add_products_to_cart(self.request)
        return Response(status=201, data=data)


class OrderView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().filter(user=self.request.user)


class OrderApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = crete_new_order(self.request)
        return Response(status=201, data=data)
