"""Описание модели аудио контента."""
from django.db import models

from . import BaseContent


class AudioContent(BaseContent):
    """Модель аудио контента."""

    bitrate = models.IntegerField()
