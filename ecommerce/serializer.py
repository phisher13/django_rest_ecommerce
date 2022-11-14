from rest_framework.serializers import ModelSerializer, \
    Serializer, ListSerializer

from .models import Product, Category, Favourite, Cart, Order


class RecursiveSerializer(Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class FilterCategorySerializer(ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CategorySerializer(ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCategorySerializer
        model = Category
        fields = ('name', 'slug', 'children')


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductFavouriteSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'total_price')


class FavouritesSerializer(ModelSerializer):
    products = ProductFavouriteSerializer(many=True)

    class Meta:
        model = Favourite
        fields = ('uuid', 'products')


class FavouritesCreateSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class ProductsForCartSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'total_price')


class CartSerializer(ModelSerializer):
    product = ProductsForCartSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
