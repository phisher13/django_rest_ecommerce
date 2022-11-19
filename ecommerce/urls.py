from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryListView,
    CategoryView,
    ProductListView,
    ProductDetailView,
    ProductView,
    ProductCreateView,
    CategoryCreateView,
    FavouriteDestroyView,
    FavouriteListView,
    FavouriteCreateView,
    CartView,
    CartApiView,
    OrderView,
    OrderApiView,
    ProductSearchESViewSet
)

router = routers.DefaultRouter()

router.register('es', ProductSearchESViewSet, basename='es-search-product')

urlpatterns = [
    # for every user
    path('product/search/', include(router.urls)),
    path('category/', CategoryListView.as_view()),
    path('product/', ProductListView.as_view()),
    path('product/<str:slug>/', ProductDetailView.as_view()),

    # for authenticated
    path('favourites/', FavouriteCreateView.as_view()),
    path('favourites/list/', FavouriteListView.as_view()),
    path('favourites/<str:uuid>', FavouriteDestroyView.as_view()),
    path('cart/info/', CartView.as_view()),
    path('cart/', CartApiView.as_view()),
    path('order/', OrderView.as_view()),
    path('order/new/', OrderApiView.as_view()),

    # for superuser
    path('category/new/', CategoryCreateView.as_view()),
    path('category/<str:slug>/', CategoryView.as_view()),
    path('product/new/', ProductCreateView.as_view()),
    path('product/<str:slug>/', ProductView.as_view()),
]
