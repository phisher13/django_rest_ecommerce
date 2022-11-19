import requests
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView, Response
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend

from .documents import ProductDocument
from .models import Category, Product, Favourite, Cart, Order
from .serializer import (
    CategorySerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CategoryCreateSerializer,
    FavouritesSerializer,
    CartSerializer,
    OrderSerializer,
    ProductDocumentSerializer,
)
from .services import (
    add_products_to_favourite,
    add_products_to_cart,
    crete_new_order,
    get_all_products,
    get_detail_product
)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(APIView):
    '''
    :methods [GET]
    :returns queryset of all products certain category
    :url '/api/v1/product?category=name_of_category'
    '''

    def get(self, request: requests) -> Response:
        data = get_all_products(self.request)
        return Response(status=200, data=data)


class ProductDetailView(APIView):
    '''
    :methods: [GET]
    :returns single object of Product instance by slug field
    :url: '/api/v1/product/<str:product_slug>'
    '''

    def get(self, request, slug) -> Response:
        data = get_detail_product(slug)
        return Response(status=200, data=data)


class CategoryView(RetrieveUpdateDestroyAPIView):
    '''
    get, update, delete certain Category instance by slug
    :methods: [GET, PUT, PATCH, DELETE]
    :permission: [IsAdmin]
    :url: '/api/v1/category/<str:slug_of_category>'
    '''
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductView(RetrieveUpdateDestroyAPIView):
    '''
    get, update, delete certain Product instance by slug
    :methods: [GET, PUT, PATCH, DELETE]
    :permission: [IsAdmin]
    :url: '/api/v1/product/<str:slug_of_product>'
    '''
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class CategoryCreateView(CreateAPIView):
    '''
    create new Category instance
    :methods: [POST]
    :permission: [IsAdmin]
    :url: '/api/v1/category/new/'
    '''
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]


class ProductCreateView(CreateAPIView):
    '''
    create new Product instance
    :methods: [POST]
    :permission: [IsAdmin]
    :url: '/api/v1/product/new/'
    '''
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class FavouriteDestroyView(DestroyAPIView):
    '''
    delete user's favourite list by uuid
    :methods: [DELETE]
    :permission: [IsAuthenticated]
    :url: '/api/v1/favourites/<str:uuid_of_favourite>'
    '''
    lookup_field = 'uuid'
    serializer_class = FavouritesSerializer

    def get_queryset(self) -> list:
        return Favourite.objects.all().filter(user=self.request.user)


class FavouriteListView(ListAPIView):
    '''
    :returns: user's favourite list
    :methods: [GET]
    :permission: [IsAuthenticated]
    :url: '/api/v1/favourites/list/'
    '''
    serializer_class = FavouritesSerializer

    def get_queryset(self) -> list:
        return Favourite.objects.all().filter(user=self.request.user)


class FavouriteCreateView(APIView):
    '''
    add products to user's favourite list
    :methods: [POST]
    :permissions: [IsAuthenticate]
    :url: '/api/v1/favourites/'
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: requests) -> Response:
        data = add_products_to_favourite(self.request)
        return Response(status=201, data=data)


class CartView(ListAPIView):
    '''
    :returns products of user's cart
    :method: [GET]
    :permission: [IsAuthenticated]
    :url: '/api/v1/cart/info/'
    '''
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> list:
        return Cart.objects.filter(user=self.request.user)


class CartApiView(APIView):
    '''
    add products to user's cart
    :method: [POST]
    :permission: [IsAuthenticated]
    :url: '/api/v1/cart/'
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: requests) -> Response:
        data = add_products_to_cart(self.request)
        return Response(status=201, data=data)


class OrderView(ListAPIView):
    '''
    :returns: user's order
    :method: [GET]
    :permission: [IsAuthenticated]
    :url: '/api/v1/order/'
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self) -> list:
        return Order.objects.all().filter(user=self.request.user)


class OrderApiView(APIView):
    '''
    create user's order
    :method: [POST]
    :permission: [IsAuthenticated]
    :url: '/api/v1/order/new/'
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: requests) -> Response:
        data = crete_new_order(self.request)
        return Response(status=201, data=data)


class ProductSearchESViewSet(DocumentViewSet):
    '''
    search product by fields: [title, description]
    :method: [GET]
    :url: '/api/v1/product/search/es?search=title:name_of_title'
    '''
    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    filter_backends = [SearchFilterBackend]
    search_fields = [
        'title',
        'description'
    ]

    filter_fields = {
        'title': 'title'
    }
