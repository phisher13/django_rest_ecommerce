from django.urls import path

from .views import (
    CategoryListView,
    CategoryView,
    ProductApiView,
    ProductView,
    ProductCreateView,
    CategoryCreateView
)

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('product/', ProductApiView.as_view()),

    # for superuser
    path('category/new/', CategoryCreateView.as_view()),
    path('category/<str:slug>/', CategoryView.as_view()),
    path('product/new/', ProductCreateView.as_view()),
    path('product/<str:slug>/', ProductView.as_view()),
]
