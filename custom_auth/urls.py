from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^jwt/create/$', Create.as_view()),
    url(r'^jwt/refresh/$', Refresh.as_view()),
    url(r'^jwt/verify/$', Verify.as_view()),

    url(r'^groups/$', GroupCreate.as_view()),
    url(r'^group/$', GroupDetail.as_view()),

    url(r'^token/appliance/$', TokenAppliance.as_view()),
    url(r'^token/$', GroupTokenCreate.as_view()),
]
