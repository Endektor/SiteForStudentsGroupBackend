from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from mail_app.views import ReactAppView


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^api/calendar/', include('calendar_app.urls')),

    url(r'^api/letters/', include('mail_app.urls')),

    url(r'^api/demosnews/', include('demos_news_app.urls')),

    url(r'^auth/', include('djoser.urls')),
    # url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('custom_auth.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns.append(url(r'^', ReactAppView.as_view()))
