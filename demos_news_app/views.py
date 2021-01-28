from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import generics

from demos_news_app.permissions import IsOwnerOrReadOnly
from .models import Post, Tag
from .serializers import *


class LocalPagination(PageNumberPagination):
    page_size = 3


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = LocalPagination

    def get_queryset(self):
        tag = self.request.GET.get('tag', 0)
        if int(tag):
            return Post.objects.filter(tag=tag).order_by('date')
        else:
            return Post.objects.all().order_by('date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated]
