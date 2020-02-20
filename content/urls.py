"""Роутинг приложения контента."""
from django.urls import include, path
from rest_framework import routers

from .resources import PageView

router = routers.DefaultRouter()
router.register(r'pages', PageView, 'pages')

urlpatterns = [
    path('', include(router.urls)),
]
