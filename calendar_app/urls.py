from django.conf.urls import url

from calendar_app import views as calendar_views


urlpatterns = [
    url(r'days/(?P<year>[0-9]{4})(?P<month>[0-9]{2})$', calendar_views.Dayslist.as_view()),
    url(r'days/(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})$', calendar_views.DayDetail.as_view()),
    url(r'info/$', calendar_views.Infolist.as_view()),
]
