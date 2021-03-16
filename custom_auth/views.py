from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate


class Create(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

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
