from rest_framework.utils import json

from .models import User
from .serializers import *
from rest_framework import status
from rest_framework.test import APITestCase


class CustomAuthApiTest(APITestCase):
    """
    It follows the way user expected to behave
    """

    def test_api(self):
        self.user_create(username='test_name', id=1)
        self.login(username='test_name')
        self.group_create()
        self.get_user_groups()
        self.get_group_users()
        self.group_token_create(role='user', expected_id=1)
        self.group_token_create(role='redactor', expected_id=2)
        tokens = self.get_group_tokens()

        self.user_create(username='test_name2', id=2)
        self.login(username='test_name2')
        self.join_to_group(token=tokens[0], role='user')
        self.join_to_group(token=tokens[1], role='redactor')

    def user_create(self, username, id):
        url = '/api/auth/users/'
        response = self.client.post(url, {'username': username,
                                          'password': 'Alpine12'})
        expected_data = {
            'email': '',
            'username': username,
            'id': id
        }
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

    def login(self, username):
        url = '/api/auth/jwt/create/'
        response = self.client.post(url, {'username': username,
                                          'password': 'Alpine12'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def group_create(self):
        url = '/api/auth/groups/'
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

    def get_user_groups(self):
        url = '/api/auth/groups/'
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

    def get_group_users(self):
        url = r'/api/auth/group/?group=group_name'
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

    def group_token_create(self, role, expected_id):
        url = '/api/auth/token/?group=group_name'
        response = self.client.post(url, {'role': role})
        expected_data = {
            'id': expected_id,
            'role': role,
            'group': 1,
            'creation_time': response.data['creation_time'],
            'token': response.data['token'],
            'token_url': 'http://localhost:8000/api/auth/token/?token=' + response.data['token']
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def get_group_tokens(self):
        url = '/api/auth/token/?group=group_name'
        response = self.client.get(url)
        expected_data = [{'id': 1,
                          'role': 'user',
                          'group': 1,
                          'creation_time': response.data[0]['creation_time'],
                          'token': response.data[0]['token']},
                         {'id': 2,
                          'role': 'redactor',
                          'group': 1,
                          'creation_time': response.data[1]['creation_time'],
                          'token': response.data[1]['token']}]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        tokens = [response.data[0]['token'], response.data[1]['token']]
        return tokens

    def join_to_group(self, token, role):
        url = '/api/auth/token/appliance/?token=' + token
        response = self.client.get(url)
        expected_data = {'id': 2,
                         'group': 1,
                         'user': 2,
                         'role': role}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
