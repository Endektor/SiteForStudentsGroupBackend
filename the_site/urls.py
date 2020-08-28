"""the_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from calendar_app import views as calendar_views
from mail_app import views as mail_views
from demos_news_app import views as demos_news_views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/days/(?P<date>[0-9]+)$', calendar_views.days_list),
    url(r'^api/info/$', calendar_views.info_list),
    url(r'^api/letters/$', mail_views.letters_list),
    url(r'^api/letters/(?P<id>[0-9]+)$', mail_views.letters_detail),
    url(r'^api/demosnews/$', demos_news_views.posts_list),
    url(r'^api/demosnews/(?P<id>[0-9]+)$', demos_news_views.posts_detail),
]
