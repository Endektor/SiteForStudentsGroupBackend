from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status

from .models import Group
from .serializers import GroupSerializer, GroupPermissionSerializer, GetGroupSerializer


class Create(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
        except AttributeError:
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

    def get_queryset(self):
        group = self.request.GET.get('group', None)
        group = Group.objects.get(name=group)
        self.queryset = self.queryset.filter(group=group)

    def perform_create(self, serializer):
        group = self.request.data.get('group')
        group = Group.objects.get(name=group)   # It cant throw an exception because it has been checked in permissions
        serializer.save(group=group)


class GroupCreate(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    queryset = Group.objects.all()
    serializer_class = GetGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
