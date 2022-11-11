import uuid

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

    def save(self, *args, **kwargs):
        self.total_price = self.price - (self.price / 100) * self.discount
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



