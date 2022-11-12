from django.contrib import admin

from .models import (
    Product,
    Category,
    Favourite
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('title', 'slug', 'total_price', 'category', 'is_available')
    search_fields = ('title', 'description', 'specification')


admin.site.register(Category)
admin.site.register(Favourite)
