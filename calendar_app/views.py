from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Day, Info, Event
from .serializers import *


@api_view(['GET'])
def days_list(request, date):
    """
    List of days or a day.
    """
    if request.method == 'GET':
        if len(date) == 6:
            year = date[0:4]
            month = date[4:]
            data = Day.objects.filter(date__year=year).filter(date__month=month)
            serializer = DaySerializer(data, context={'request': request}, many=True)

        else:
            try:
                day = Day.objects.get(date__year=date[0:4], date__month=date[4:6], date__day=date[6:8])
            except Day.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = DaySerializer(day, context={'request': request})
        return Response({'data': serializer.data})


@api_view(['GET'])
def info_list(request):
    """
    List info models.
    """
    if request.method == 'GET':
        data = Info.objects.all()
        serializer = InfoSerializer(data, context={'request': request}, many=True)
        return Response({'data': serializer.data})
