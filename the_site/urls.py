from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^api/calendar/', include('calendar_app.urls')),

    url(r'^api/letters/', include('mail_app.urls')),

    url(r'^api/demosnews/', include('demos_news_app.urls')),

    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
]
