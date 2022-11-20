import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .. import models
from .. import serializer as serializers


class TestCategoryView(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin'
        )
        self.token = self.client.post('/auth/jwt/create/', data={
            'username': 'admin',
            'password': 'admin'
        })
        self.jwt = {}
        for i in self.token:
            self.jwt = json.loads(i.decode('utf-8'))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt['access'])

    def test_get_all_categories(self):
        response = self.client.get('/api/v1/category/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {
            'name': 'test_category'
        }

        response = self.client.post('/api/v1/category/new/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail_category(self):
        data = {
            'name': 'test_category'
        }

        self.client.post('/api/v1/category/new/', data=data)

        category = models.Category.objects.get(name='test_category')

        response = self.client.get(f'/api/v1/category/{category.slug}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        data = {
            'name': 'test_category'
        }

        self.client.post('/api/v1/category/new/', data=data)

        category = models.Category.objects.get(name='test_category')

        response = self.client.delete(f'/api/v1/category/{category.slug}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_category(self):
        data = {
            'name': 'test_category'
        }
        upd_data = {
            'name': 'test_category_upd'
        }

        self.client.post('/api/v1/category/new/', data=data)

        category = models.Category.objects.get(name=data['name'])

        response = self.client.patch(f'/api/v1/category/{category.slug}/', data=upd_data)

        upd_category = models.Category.objects.filter(name=upd_data['name']).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(upd_category, True)
