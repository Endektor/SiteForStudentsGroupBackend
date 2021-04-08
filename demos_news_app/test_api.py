from custom_auth.test_api import CustomAuthApiTest
from rest_framework import status


class PostsApiTest(CustomAuthApiTest):

    def test_api(self):
        self.user_create(username='name1', id=1)
        self.login(username='name1')
        self.group_create()
        self.post_create()
        self.tag_create()

    def post_create(self):
        url = '/api/demosnews/posts/'
        response = self.client.post(url, {'title': 'test_title1',
                                          'text': 'test_title1',
                                          'date': '2013-01-29T12:34:56.000000Z',
                                          'user': 1,
                                          'group': 'group_name'})
        expected_data = {'id': 1,
                         'title': 'test_title1',
                         'text': 'test_title1',
                         'date': '2013-01-29T16:34:56+04:00',
                         'user': {'id': 1, 'username': 'name1'},
                         'post_tags': []}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

    def tag_create(self):
        url = '/api/demosnews/tags/'
        response = self.client.post(url, {'name': 'test_name',
                                          'post': 1,
                                          'group': 'group_name'})
        expected_data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)
