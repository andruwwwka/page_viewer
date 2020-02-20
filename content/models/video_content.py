"""Описание моделей видеоконтента."""
from django.db import models

from . import BaseContent


class VideoContent(BaseContent):
    """Модель видео контента."""

    video_file = models.URLField()
    subs = models.URLField(blank=True, null=True)
