from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^letters/$', LettersList.as_view()),
    url(r'^letters/(?P<id>[0-9]+)$', LetterDetail.as_view()),

    url(r'^check_email/(?P<amount>[0-9]+)$', CheckEmail.as_view()),

    url(r'^upload/$', UploadFiles.as_view()),
]
