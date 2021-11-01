from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .models import Day, Info, Event
from .serializers import *


class Dayslist(generics.ListAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
        return Day.objects.filter(date__year=year, date__month=month)


class DayDetail(generics.RetrieveAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    lookup_field = 0
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]


class GetSchedule(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self):
        from icalendar import Calendar

        with open('M4O.ics', 'rb') as ics_file:
            calendar = Calendar.from_ical(ics_file.read())

        for component in calendar.walk():
            if component.name == "VEVENT":
                start_datetime = component.get('dtstart').dt

                date_obj = Day.objects.get_or_create(date=start_datetime.date())
                event_obj = Event.objects.get_or_create(description=component.get('summary'),
                                                        day=date_obj,
                                                        event_info=Info.objects.get(topic="Пара"),
                                                        time=start_datetime)


# class TagDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     lookup_field = 'id'
#     permission_classes = [permissions.DjangoObjectPermissions, permissions.IsAuthenticated]
