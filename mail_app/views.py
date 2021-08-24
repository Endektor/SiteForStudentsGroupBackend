from django.views.generic import View
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from .models import Letter
from .serializers import *
from .mail_service import Service

import os


class LocalPagination(PageNumberPagination):
    page_size = 10


class LettersList(generics.ListCreateAPIView):
    queryset = Letter.objects.all().order_by('-date_time')
    serializer_class = LetterSerializer
    pagination_class = LocalPagination
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated]


class LetterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'id'
    #permission_classes = [permissions.IsAuthenticated]


class CheckEmail(View):

    @staticmethod
    def get(request, *args, **kwargs):
        service = Service()
        service.get_mails()
        return HttpResponse(1)


class ReactAppView(View):

    def get(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )