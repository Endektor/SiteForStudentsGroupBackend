from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

from demos_news_app.models import Post
from demos_news_app.serializers import PostSerializer


class PostsApiTestCase(TestCase):

    def get_test_list(self):
        post1 = Post.objects.create(title='test_title1',
                                    text='test_title1',
                                    date=timezone.now,
                                    author=User.objects.get(id=1))
        post2 = Post.objects.create(title='test_title2',
                                    text='test_title2',
                                    date=timezone.now,
                                    author=User.objects.get(id=1))
        url = reverse('demosnews-PostList')
        print(url)
        response = self.client.get(url)
        serializer_data = PostSerializer([post1, post2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # def get_test(self):
    #     post1 = Post.objects.create(title='test_title1',
    #                                 text='test_title1',
    #                                 date=timezone.now,
    #                                 author=User.objects.get(id=1))
    #     post2 = Post.objects.create(title='test_title2',
    #                                 text='test_title2',
    #                                 date=timezone.now,
    #                                 author=User.objects.get(id=10))
    #     url = reverse('demosnews-PostList')
    #     print(url)
    #     response = self.client.get(url)
    #     serializer_data = PostSerializer([post1, post2], many=True)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(serializer_data, response.data)


