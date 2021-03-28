from rest_framework.utils import json

from .models import Group, GroupPermission, User
from .serializers import *
from rest_framework import status
from rest_framework.test import APITestCase


class AuthApiTest(APITestCase):

    def user_create(self):
        url = '/auth/users/'
        response = self.client.post(url, {'username': 'test_name',
                                          'password': 'Alpine12'})
        expected_data = {
            'email': '',
            'username': 'test_name',
            'id': 1
        }
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)
        user = User.objects.get(username='test_name')
        user.is_active = True
        user.save()

    def token_create(self):
        url = '/api/jwt/create/'
        response = self.client.post(url, {'username': 'test_name',
                                          'password': 'Alpine12'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.access = response.data['access']

    def group_create(self):
        url = '/api/group/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        response = self.client.post(url, {'name': 'group_name'})
        expected_data = {
            "id": 1,
            "name": "group_name",
            "users": [
                1
            ]
        }
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_api(self):
        self.user_create()
        self.token_create()
        self.group_create()
    #     # group_1 = Group.objects.create(name='test1')
    #     # group_2 = Group.objects.create(name='test2')
    #     user_1 = User.objects.create(username='user1', password='password1')
    #     user_2 = User.objects.create(username='user2', password='password2')
    #     user_1.is_active = True
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)
    #     user_2.is_active = True
    #     # group_permission_1 = GroupPermission.objects.create(date='2020-09-01', topic='Day1')
    #     # group_permission_2 = GroupPermission.objects.create(date='2020-09-02', topic='Day2')
    #     create_group = '/auth/group/'
    #     response = self.client.post(create_group, {'name': 'group_name'})
    #     expected_data = """
    #     {
    #         'id': 1,
    #         'name': 'group_name',
    #         'users': [
    #             1
    #         ]
    #     }
    #     """
    #     expected_data = json.dumps(expected_data)
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     self.assertEqual(expected_data, response.data)
