from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


from .models import BlackList, WhiteList


class Create(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': "User does not exist or password is incorrect"}, status=400)

        refresh = RefreshToken.for_user(user)
        WhiteList(refresh_token=refresh, user=user).save()
        response = Response({'access': str(refresh.access_token)}, status=201)
        response.set_cookie(
            'refresh',
            str(refresh),
            max_age=15 * 24 * 60 * 60,
            path="/auth",
            samesite="lax",
            secure=True,
            httponly=True, )
        return response


class Refresh(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        refresh_old = request.COOKIES.get('refresh', None)

        if not refresh_old:
            return Response({'error': "No refresh token"}, status=401)

        try:
            BlackList.objects.get(refresh_token=refresh_old)
            return Response({'error': "Refresh token is in blacklist. Possibly somebody has stolen your credentials. You should check your computer for viruses"}, status=401)
        except ObjectDoesNotExist:
            pass

        try:
            refresh_old_obj = WhiteList.objects.get(refresh_token=refresh_old)
            refresh_old_obj.delete()
            BlackList(refresh_token=refresh_old).save()
        except ObjectDoesNotExist:
            return Response({'error': "Refresh token is not in whitelist"}, status=401)

        try:
            user_id = RefreshToken(refresh_old).get('user_id')
            user = User.objects.get(id=user_id)
            refresh = RefreshToken().for_user(user)
            WhiteList(refresh_token=refresh, user=user).save()
            print(refresh)
            print(refresh_old)
        except TokenError:
            return Response({'error': "Invalid refresh token"}, status=400)

        response = Response({'access': str(refresh.access_token)}, status=200)
        response.set_cookie(
            'refresh',
            str(refresh),
            max_age=15 * 24 * 60 * 60,
            path="/auth",
            secure=True,
            samesite="lax",
            httponly=True, )
        return response


class Verify(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        access = request.POST['access']
        try:
            AccessToken(access)
        except TokenError:
            return Response({'error': "Invalid access token"}, status=400)

        response = Response({'result': "OK"}, status=200)
        return response


class RejectRefresh(APIView):
    def get(self, request, *args, **kwargs):
        refresh_old = request.COOKIES.get('refresh', None)
        try:
            refresh_old_obj = WhiteList.objects.get(refresh_token=refresh_old)
            refresh_old_obj.delete()
        except ObjectDoesNotExist:
            pass
        if not refresh_old:
            BlackList(refresh_token=refresh_old).save()
        return Response('OK', status=200)
