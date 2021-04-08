from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views import View
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from rest_framework.response import Response

from decouple import config
import pyAesCrypt

from .models import Letter
from .serializers import *
from .mail_service import Service
from custom_auth.permissions import IsOwnerOrReadOnly, IsGroupRedactorOrReadOnly, IsGroupMember, IsGroupAdmin
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
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class LetterDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and destroy letter
    """
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsGroupRedactorOrReadOnly]


class CheckEmail(GroupListCreateAPIView):
    """
    Checks latest letters on the group's mail
    """
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

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
    def save_file(fs, name, file, folder):
        if fs.exists(name):
            fs.delete(name)
        fs.save(name, file)

        buffer_size = 64 * 1024
        key = config('KEY')
        file_name = folder + name
        pyAesCrypt.encryptFile(file_name, file_name + '.aes', key, buffer_size)
        fs.delete(name)

    def post(self, request, *args, **kwargs):
        folder = 'mail_app/group_files/' + self.get_group_name() + '/'

        try:
            credentials = request.FILES['credentials.json']
            token = request.FILES['token.json']
        except MultiValueDictKeyError:
            return Response('There is no credentials.json or token.json file', status=400)

        fs = FileSystemStorage(location=folder)
        self.save_file(fs, 'credentials.json', credentials, folder)
        self.save_file(fs, 'token.json', token, folder)
        return Response('Saved', status=200)
