"""Описание моделей текстового контента."""
from django.db import models

from . import BaseContent


class TextContent(BaseContent):
    """Модель текстового контента."""

    body = models.TextField()
