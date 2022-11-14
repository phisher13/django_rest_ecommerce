import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField('Title', max_length=255, null=False, blank=False)
    slug = models.SlugField('Slug', unique=True, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    specification = models.JSONField(null=False, blank=False)
    images = models.JSONField(null=True, blank=True)
    price = models.IntegerField(null=False, blank=False)
    discount = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-date']

    @staticmethod
    def count(price, discount=None):
        if discount:
            return int(price - ((price / 100) * discount))
        return price

    def save(self, *args, **kwargs):
        self.total_price = Product.count(self.price, self.discount)
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.uuid}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Category(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children')

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.uuid}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Favourite(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    products = models.ManyToManyField(Product,
                                      null=False,
                                      blank=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='favourites')

    class Meta:
        db_table = 'favourite'
        verbose_name = 'favourite'
        verbose_name_plural = 'favourites'

    def __str__(self):
        return f'{self.user}: {[i.title for i in self.products.all()]}'


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='cart')
    quantity = models.IntegerField(null=False, blank=False, default=1)
    amount = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def save(self, *args, **kwargs):
        self.amount = (self.product.total_price * self.quantity)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'
