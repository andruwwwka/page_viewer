"""pages_viewer URL Configuration."""
from django.contrib import admin
from django.urls import include, path

from content import urls as content_urls  # noqa I100, I202

urlpatterns = [
    path('api/', include(content_urls)),
    path('admin/', admin.site.urls),
]
