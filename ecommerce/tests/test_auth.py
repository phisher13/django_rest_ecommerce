from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class TestUserAuthentication(APITestCase):
    def test_register(self):
        data = {
            'username': 'test_username1',
            'email': 'test_email@tests.com',
            'password': 'test_password'
        }

        response = self.client.post('/auth/users/', data=data)
        new_user = User.objects.filter(username=data['username']).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_user.email, data['email'])

    def test_login(self):
        data_reg = {
            'username': 'test_username1',
            'email': 'test_email@tests.com',
            'password': 'test_password'
        }

        self.client.post('/auth/users/', data=data_reg)

        data_log = {
            'username': 'test_username1',
            'password': 'test_password'
        }

        response = self.client.post('/auth/token/login/', data=data_log)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
