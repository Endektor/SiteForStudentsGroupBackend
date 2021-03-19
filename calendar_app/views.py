from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions

from .models import Day, Info, Event
from .serializers import *
from custom_auth.permissions import IsOwnerOrReadOnly, IsGroupMember, IsObjectInUsersGroup
from custom_auth.models import Group
from custom_auth.views import GroupListCreateAPIView


class Dayslist(GroupListCreateAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        super(Dayslist, self).get_queryset()
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        self.queryset = self.queryset.filter(date__year=year, date__month=month)
        return self.queryset


class DayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    lookup_field = 0
    permission_classes = [permissions.IsAuthenticated, IsGroupMember, IsOwnerOrReadOnly]

    def get_object(self):
        queryset = self.get_queryset()
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        day = self.kwargs.get('day', 0)
        obj = get_object_or_404(queryset, date__year=year, date__month=month, date__day=day)
        return obj


class Infolist(GroupListCreateAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

# class TagDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     lookup_field = 'id'
#     permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated]
