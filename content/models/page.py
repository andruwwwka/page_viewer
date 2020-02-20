"""Описание модели страницы контента."""
from . import CommonInfo


class Page(CommonInfo):
    """Модель страницы."""

    class Meta:  # noqa D106
        ordering = ('-id', )
