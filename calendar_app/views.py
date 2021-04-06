from django.utils.datetime_safe import datetime
from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Day, Info, Event
from .serializers import *
from custom_auth.permissions import IsGroupRedactorOrReadOnly
from custom_auth.views import GroupListCreateAPIView


class DayList(GroupListCreateAPIView):
    """
    List of days or day creation
    """
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]

    def get_queryset(self):
        super(DayList, self).get_queryset()
        year = self.request.GET.get('year', None)
        month = self.kwargs.get('month', None)
        if not year:
            year = datetime.year
        if not month and month != 0:
            month = datetime.month

        self.queryset = self.queryset.filter(date__year=year, date__month=month)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = DaySerializer(data={'date': request.POST.get('date', None),
                                         'topic': request.POST.get('topic', None)})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DayDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Operations with concrete day
    """
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]

    def get_object(self):
        year = self.request.POST.get('year', 0)
        month = self.request.POST.get('month', 0)
        day = self.request.POST.get('day', 0)
        obj = get_object_or_404(self.get_queryset,
                                date__year=year,
                                date__month=month,
                                date__day=day)
        return obj


class EventList(GroupListCreateAPIView):
    """
    List of events or event creation
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Operations with concrete event
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class InfoList(GroupListCreateAPIView):
    """
    List of infos or info creation
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class InfoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Operations with concrete info
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]
