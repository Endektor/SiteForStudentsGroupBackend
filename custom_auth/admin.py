from django.contrib import admin
from .models import BlackList, WhiteList


admin.site.register(BlackList)
admin.site.register(WhiteList)
