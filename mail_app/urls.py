from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', LetterDetail.as_view()),
    url(r'^check_email/(?P<id>[0-9]+)$', CheckEmail.as_view()),
    url(r'^$', LettersList.as_view()),
]
