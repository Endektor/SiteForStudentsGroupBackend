from django.http import HttpResponse
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from .models import Letter
from .serializers import *

from .mail_service import Service


class LocalPagination(PageNumberPagination):
    page_size = 10


class LettersList(generics.ListCreateAPIView):
    queryset = Letter.objects.all().order_by('-date_time')
    serializer_class = LetterSerializer
    pagination_class = LocalPagination
    # permission_classes = [permissions.IsAuthenticated]


class LetterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'id'
    # permission_classes = [permissions.IsAuthenticated]


class CheckEmail(View):

    @staticmethod
    def get(request, *args, **kwargs):
        service = Service(amount_of_letters=kwargs['id'])
        service.get_mails()
        return HttpResponse(1)
