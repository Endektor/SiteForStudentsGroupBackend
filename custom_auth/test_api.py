from rest_framework.utils import json

from icecream import ic

from .models import Group, GroupPermission, User
from .serializers import *
from rest_framework import status
from rest_framework.test import APITestCase


def print_decorator(func):
    def wrapper(self):
        print('Test: {}'.format(func.__name__), end='')
        func(self)
        print(' OK')
    return wrapper


class CustomAuthApiTest(APITestCase):

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

    @print_decorator
    def user_create(self, name):
        url = '/api/auth/users/'
        response = self.client.post(url, {'username': name,
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

    @print_decorator
    def token_create(self):
        url = '/api/auth/jwt/create/'
        response = self.client.post(url, {'username': 'test_name',
                                          'password': 'Alpine12'})
        self.access = response.data['access']
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    @print_decorator
    def group_create(self):
        url = '/api/auth/group/'
        self.auth(self.access)
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

    @print_decorator
    def get_user_groups(self):
        url = '/api/auth/group/'
        self.auth(self.access)
        response = self.client.get(url)
        expected_data = [
            {
                "id": 1,
                "name": "group_name",
                "users": [
                    1
                ]
            }
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    @print_decorator
    def get_group_users(self):
        url = '/api/auth/group/group_name'
        self.auth(self.access)
        response = self.client.get(url)
        expected_data = {
            "id": 1,
            "name": "group_name",
            "users": [
                {
                    "id": 1,
                    "username": "test_name"
                }
            ]
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    @print_decorator
    def group_token_create(self):
        url = '/api/auth/token/?group=group_name'
        self.auth(self.access)

        def test(role, expected_id):
            response = self.client.post(url, {'role': role})
            expected_data = {
                'id': expected_id,
                'role': role,
                'group': 1,
                'creation_time': response.data['creation_time'],
                'token': response.data['token']
            }
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(expected_data, response.data)
        test('user', 1)
        test('redactor', 2)

    @print_decorator
    def join_to_group(self):
        pass

    def test_api(self):
        self.user_create('test_name')
        self.token_create()
        self.group_create()
        self.get_user_groups()
        self.get_group_users()
        self.group_token_create()

        self.user_create('test_name2')
        self.join_to_group()

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
