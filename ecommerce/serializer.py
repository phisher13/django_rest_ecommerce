from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer

from .models import Product, Category


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
        fields = ('name', 'children')


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
