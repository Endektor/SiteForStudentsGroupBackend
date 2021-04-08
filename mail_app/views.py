from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views import View
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Letter
from .serializers import *
from .mail_service import Service
from custom_auth.permissions import IsOwnerOrReadOnly, IsGroupMember, IsGroupAdmin
from custom_auth.models import Group
from custom_auth.views import GroupListCreateAPIView


class LocalPagination(PageNumberPagination):
    page_size = 10


class LettersList(GroupListCreateAPIView):
    """
    List of letters
    """
    queryset = Letter.objects.all().order_by('-date_time')
    serializer_class = LetterSerializer
    pagination_class = LocalPagination
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]


class LetterDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and destroy letter
    """
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsGroupAdmin]


class CheckEmail(GroupListCreateAPIView):
    """
    Checks latest letters on the group's mail
    """
    def get(self, request, *args, **kwargs):
        group = self.get_group_name()
        service = Service(amount_of_letters=kwargs['amount'], group=group)
        service.start()
        return HttpResponse(1)


class UploadFiles(GroupListCreateAPIView):
    """
    Saves credentials.json and token.json to group's folder
    """
    permission_classes = [permissions.IsAuthenticated, IsGroupAdmin]

    @staticmethod
    def save_file(fs, name, file):
        if fs.exists(name):
            fs.delete(name)
        fs.save(name, file)

    def post(self, request, *args, **kwargs):
        folder = 'mail_app/group_files/' + self.get_group_name() + '/'

        try:
            credentials = request.FILES['credentials.json']
            token = request.FILES['token.json']
        except MultiValueDictKeyError:
            return Response('There is no credentials.json or token.json file', status=400)
        fs = FileSystemStorage(location=folder)
        self.save_file(fs, 'credentials.json', credentials)
        self.save_file(fs, 'token.json', token)
        return Response(1, status=200)
