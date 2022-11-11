from django.urls import path

from .views import ProductListView, ProductView

urlpatterns = [
    path('product/', ProductListView.as_view()),
    path('product/<str:slug>', ProductView.as_view()),
]
