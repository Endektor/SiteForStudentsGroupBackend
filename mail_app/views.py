from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from .models import Letter
from .serializers import *


class LocalPagination(PageNumberPagination):
    page_size = 2


class LettersList(generics.ListCreateAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    pagination_class = LocalPagination
    permission_classes = [permissions.IsAuthenticated]


class LetterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
