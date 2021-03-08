from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from custom_auth import views as auth_views

urlpatterns = [
    url('jwt/create/$', auth_views.Create.as_view()),
    url('jwt/refresh/$', auth_views.Refresh.as_view()),
    url('jwt/verify/$', auth_views.Verify.as_view()),
]
