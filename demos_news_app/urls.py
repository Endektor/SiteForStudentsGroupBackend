from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^posts/$', PostList.as_view()),
    url(r'^posts/(?P<id>[0-9]+)$', PostDetail.as_view()),

    url(r'^tags/$', TagList.as_view()),
    url(r'^tags/(?P<id>[0-9]+)$', TagDetail.as_view()),
]