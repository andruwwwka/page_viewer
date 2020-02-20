"""Базовые модели приложения."""
from django.db import models


class CommonInfo(models.Model):
    """Базовая абстрактная модель для всех моделей приложения."""

    title = models.CharField(max_length=256)

    class Meta:  # noqa D106
        abstract = True

    def __str__(self):
        """Строковое представление для моделей с заголовком."""
        return f'{self.title} ({self.id})'


class BaseContent(CommonInfo):
    """Базовая модель для моделей котента (обязательна к наследованию)."""

    order = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='items')

    class Meta:  # noqa D106
        ordering = ('order', )
