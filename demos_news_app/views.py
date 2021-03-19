from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, generics

from custom_auth.permissions import IsOwnerOrReadOnly, IsGroupMember, IsObjectInUsersGroup
from custom_auth.models import Group
from custom_auth.views import GroupListCreateAPIView
from rest_framework.response import Response

from .models import Post, Tag
from .serializers import *


class LocalPagination(PageNumberPagination):
    page_size = 5


class PostList(GroupListCreateAPIView):
    queryset = Post.objects.all().order_by('date')
    serializer_class = PostSerializer
    pagination_class = LocalPagination
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        super(PostList, self).get_queryset()
        tags = self.request.GET.get('tags', None)

        try:
            tags = tags.split(',')
            tags = list(map(int, tags))
            self.queryset = self.queryset.filter(tag__in=tags)
            return self.queryset

        except (ValueError, AttributeError):
            return self.queryset

    def perform_create(self, serializer):
        tags = self.request.data.get('tags', None)
        group = self.request.data.get('group')
        group = Group.objects.get(name=group)   # It cant throw an exception because it has been checked in permissions
        if tags:
            tags = list(map(int, tags.split(',')))
            tags = Tag.objects.filter(id__in=tags)
            serializer.save(author=self.request.user, group=group, tags=tags)
        else:
            serializer.save(author=self.request.user, group=group)


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


class TagList(GroupListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated, IsGroupMember]
