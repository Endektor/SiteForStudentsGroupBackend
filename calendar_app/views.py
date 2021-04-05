from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions

from .models import Day, Info, Event
from .serializers import *
from custom_auth.permissions import IsGroupRedactorOrReadOnly
from custom_auth.views import GroupListCreateAPIView


class Daylist(GroupListCreateAPIView):
    """
    List of posts or post creation
    """
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]

    def get_queryset(self):
        super(Daylist, self).get_queryset()
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        self.queryset = self.queryset.filter(date__year=year, date__month=month)
        return self.queryset


class DayDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Operations with concrete post
    """
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    lookup_field = 0
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]

    def get_object(self):
        queryset = self.get_queryset()
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        day = self.kwargs.get('day', 0)
        obj = get_object_or_404(queryset, date__year=year, date__month=month, date__day=day)
        return obj


class Infolist(GroupListCreateAPIView):
    """
    List of posts or post creation
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class InfoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Operations with concrete post
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]
