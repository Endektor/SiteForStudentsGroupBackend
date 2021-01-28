from rest_framework.generics import get_object_or_404
from rest_framework import generics

from .models import Day, Info, Event
from .serializers import *


class Dayslist(generics.ListAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    def get_queryset(self):
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        print(month, year)
        return Day.objects.filter(date__year=year, date__month=month)


class DayDetail(generics.RetrieveAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    lookup_field = 0

    def get_object(self):
        queryset = self.get_queryset()
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        day = self.kwargs.get('day', 0)
        obj = get_object_or_404(queryset, date__year=year, date__month=month, date__day=day)
        return obj


class Infolist(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


# class TagDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     lookup_field = 'id'
#     permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated]
