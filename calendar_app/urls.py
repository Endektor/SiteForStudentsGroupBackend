from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^days/$', DayList.as_view()),
    url(r'^day/$', DayDetail.as_view()),

    url(r'^events/$', EventList.as_view()),
    url(r'^event/$', EventDetail.as_view()),

    url(r'^infos/$', InfoList.as_view()),
    url(r'^info/$', InfoDetail.as_view()),
]
