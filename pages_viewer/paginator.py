"""Пагинация приложения."""
from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Переопределенный стандартный класс пагинации для возможности опрдеелять количество элементов на странице."""

    page_size_query_param = 'per_page'
