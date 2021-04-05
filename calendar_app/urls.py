from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^days/(?P<year>[0-9]{4})(?P<month>[0-9]{2})$', Daylist.as_view()),
    url(r'^days/(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})$', DayDetail.as_view()),

    url(r'^info/$', Infolist.as_view()),
]
