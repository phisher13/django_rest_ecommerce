from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        setting = {
            'numbers_of_shards': 1,
            'numbers_of_replicas': 0,
        }

    class Django:
        model = Product
        fields = [
            'title',
            'description'
        ]
