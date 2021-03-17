from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import generics

from demos_news_app.permissions import IsOwnerOrReadOnly, IsGroupMember, IsObjectInUsersGroup
from .models import Post, Tag
from custom_auth.models import Group
from .serializers import *

from icecream import ic


class LocalPagination(PageNumberPagination):
    page_size = 5


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = LocalPagination
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        tags = self.request.GET.get('tags', None)
        group = self.request.GET.get('group', None)
        group = Group.objects.get(name=group)
        self.queryset = self.queryset.filter(group=group)

        try:
            tags = tags.split(',')
            tags = list(map(int, tags))
            self.queryset = self.queryset.filter(tag__in=tags)
            return self.queryset

        except (ValueError, AttributeError):
            return self.queryset

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
    permission_classes = [permissions.IsAuthenticated, IsGroupMember, IsOwnerOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        group = self.request.GET.get('group', None)
        group = Group.objects.get(name=group)
        self.queryset = self.queryset.filter(group=group)

        return self.queryset


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated, IsGroupMember]
