from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    url('jwt/create/$', Create.as_view()),
    url('jwt/refresh/$', Refresh.as_view()),
    url('jwt/verify/$', Verify.as_view()),

    url(r'group/$', GroupCreate.as_view()),
    url(r'group/(?P<name>[a-zA-Z0-9_]+)$', GroupDetail.as_view()),
    url(r'token/$', CreateGroupToken.as_view()),
]
