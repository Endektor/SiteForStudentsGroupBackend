from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import generics

from demos_news_app.permissions import IsOwnerOrReadOnly
from .models import Post, Tag
from .serializers import *

from icecream import ic


class LocalPagination(PageNumberPagination):
    page_size = 3


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = LocalPagination

    def get_queryset(self):
        tags = self.request.GET.get('tags', 'error')

        try:
            tags = tags.split(',')
            tags = list(map(int, tags))
            posts = Post.objects.filter(tags__in=tags)
            return posts.order_by('date')

        except ValueError:
            return Post.objects.all().order_by('date')

    def perform_create(self, serializer):
        tags = self.request.data.get('tags', None)
        if tags:
            tags = list(map(int, tags.split(',')))
            tags = Tag.objects.filter(id__in=tags)
            serializer.save(author=self.request.user, tags=tags)
        else:
            serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        tags = request.data.get('tags', None)
        if tags:
            tags = list(map(int, tags.split(',')))
            post = Post.objects.get(id=kwargs.get('id'))
            post.tags.set(Tag.objects.filter(id__in=tags))
            post.save()

        return self.update(request, *args, **kwargs)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated]
