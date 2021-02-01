from django.conf.urls import url

from mail_app import views as mail_views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', mail_views.LetterDetail.as_view()),
    url(r'^check_email/(?P<id>[0-9]+)$', mail_views.CheckEmail.as_view()),
    url('^$', mail_views.LettersList.as_view()),
]
