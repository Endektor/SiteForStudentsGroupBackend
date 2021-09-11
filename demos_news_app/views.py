from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions

from demos_news_app.permissions import IsOwnerOrReadOnly
from .models import Post, Tag
from .serializers import *


class LocalPagination(PageNumberPagination):
    page_size = 1000


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer
    pagination_class = LocalPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tags = self.request.GET.get('tags', None)
        if tags:
            tags = tags.split(',')
            tags = [tag.strip() for tag in tags]
            posts = self.queryset.filter(tags__name__in=tags)
            return posts

        else:
            return self.queryset

    def perform_create(self, serializer):
        tags_objs = self.create_tags()
        if tags_objs:
            serializer.save(author=self.request.user, tags=tags_objs)
        else:
            serializer.save(author=self.request.user)

    def create_tags(self):
        tags = self.request.data.get('tags', None)
        if tags:
            tags = tags.split(',')
            tags = [tag.strip() for tag in tags]
            tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags]
            return tags_objs


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        tags = request.data.get('tags', None)
        if tags:
            tags = tags.split(',')
            tags = [tag.strip() for tag in tags]
            tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags]
            post = Post.objects.get(id=kwargs.get('id'))
            post.tags.set(tags_objs)
            post.save()

        return self.update(request, *args, **kwargs)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'name'
    permission_classes = [permissions.IsAuthenticated]
