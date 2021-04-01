from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta

from .models import Group, GroupToken
from .serializers import *
from .permissions import IsGroupAdmin

username = openapi.Schema(title='username', type='string')
password = openapi.Schema(title='password', type='string')
response_schema_dict = openapi.Schema(title='lol', type='object',
                                      properties={'username': username, 'password': password})


class Create(generics.GenericAPIView):
    """
    Authentication
    returns refresh token in cookies and access token in body
    """
    serializer_class = TokenSerializer  # delete
    permission_classes = []

    @swagger_auto_schema(request_body=response_schema_dict)
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username:    # used by swagger, delete later
            username = request.data['username']     # delete
            password = request.data['password']     # delete

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': "User does not exist or password is incorrect"}, status=400)

        refresh = RefreshToken.for_user(user)
        response = Response({'access': str(refresh.access_token)}, status=201)
        response.set_cookie(
            'refresh',
            str(refresh),
            max_age=60 * 24 * 60 * 60,
            # domain=,
            # secure=settings.SESSION_COOKIE_SECURE or None,
            httponly=True, )
        return response


class Refresh(APIView):
    """
    Refresh of access token
    returns new access token in body
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_old = request.COOKIES.get('refresh', None)
        try:
            refresh = RefreshToken(refresh_old)
            print(refresh.get('username'))
        except TokenError:
            return Response({'error': "Invalid refresh token"}, status=400)

        response = Response({'access': str(refresh.access_token)}, status=200)
        return response


class Verify(APIView):
    """
    Verification of access token
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        access = request.POST['access']
        try:
            refresh = AccessToken(access)
        except TokenError:
            return Response({'error': "Invalid access token"}, status=400)

        response = Response({'result': "OK"}, status=200)
        return response


class GroupListCreateAPIView(generics.ListCreateAPIView):
    """
    Modified ListCreateAPIView for groups
    sorts all models by group and automatically adds group to models while creation
    """
    def get_group(self):
        group = self.request.GET.get('group', None)
        group = Group.objects.get(name=group)   # It cant throw an exception because it has been checked in permissions
        return group

    def get_queryset(self):
        self.queryset = self.queryset.filter(group=self.get_group())

    def perform_create(self, serializer):
        serializer.save(group=self.get_group())


class GroupCreate(generics.ListCreateAPIView):
    """
    List of user's groups or group creation
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        self.queryset = self.request.user.users_in_group.all()
        return self.queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'users': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        group = self.perform_create(serializer)

        serializer_role = GroupPermissionSerializer(data={'group': group.id,
                                                          'user': request.user.id,
                                                          'role': 'admin'})
        serializer_role.is_valid(raise_exception=True)
        self.perform_create(serializer_role)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        group = serializer.save()
        return group


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and destroy group
    """
    queryset = Group.objects.all()
    serializer_class = GetGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'


class CreateGroupToken(generics.GenericAPIView):
    """
    Invitation to group token
    returns token and adds user to group using token
    """
    permission_classes = {'GET': [permissions.IsAuthenticated],
                          'POST': [permissions.IsAuthenticated, IsGroupAdmin]}

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permission() for permission in self.permission_classes['GET']]
        else:
            return [permission() for permission in self.permission_classes['POST']]

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', None)
        if not token:
            return Response({'error': "No token provided"}, status=400)
        try:
            token = GroupToken.objects.get(token=token)
        except GroupToken.DoesNotExist:
            return Response({'error': "Token does not exist or is invalid"}, status=400)

        if timezone.now() - token.creation_time >= timedelta(days=7):
            token.delete()
            return Response({'error': "Token does not exist or is invalid"}, status=400)

        role_obj, created = GroupPermission.objects.get_or_create(group=token.group,
                                                                  user=request.user,
                                                                  defaults={'role': token.role})
        if role_obj.role == 'admin':
            return Response({'error': "You are admin here"}, status=400)
        elif role_obj.role != token.role:
            role_obj.role = token.role
            role_obj.save()
        role_serializer = GroupPermissionSerializer(role_obj)
        return Response(role_serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        role = request.POST.get('role', None)
        group = request.GET.get('group', None)
        group = Group.objects.get(name=group)
        if role not in ('redactor', 'user'):
            return Response({'error': "Select a valid role"}, status=400)

        token = GroupTokenSerializer(data={'role': role, 'group': group.id})
        token.is_valid(raise_exception=True)
        token.save()
        host = request.META['HTTP_HOST']
        token_dict = dict(token.data)
        token_dict['token'] = 'http://' + host + '/api/auth/token/?token=' + token_dict['token']
        return Response(token_dict, status=200)
