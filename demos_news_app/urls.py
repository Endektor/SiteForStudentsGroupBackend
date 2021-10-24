from django.conf.urls import url

from demos_news_app import views as demos_news_views

urlpatterns = [
    url('posts/$', demos_news_views.PostList.as_view()),
    url(r'posts/(?P<id>[0-9]+)$', demos_news_views.PostDetail.as_view()),
    url('tags/$', demos_news_views.TagList.as_view()),
    url(r'tags/(?P<name>[a-zA-Z0-9]+)$', demos_news_views.TagDetail.as_view()),
]
