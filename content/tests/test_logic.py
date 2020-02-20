"""Тесты логики приложения."""
from django.db import IntegrityError
from django.test.testcases import TestCase

from ..models import BaseContent, Page


class TestLogic(TestCase):
    """Тесты логики."""

    def setUp(self):
        """Подготовка тестовых данных."""
        super().setUp()
        self.page = Page.objects.create(title='Test page')
        self.content = BaseContent.objects.create(
            title='Test content',
            page=self.page,
        )

    def test_cannot_create_content_without_page(self):
        """Тест невозможности создания контента без страницы."""
        with self.assertRaises(IntegrityError):
            BaseContent.objects.create(
                title='Base content',
            )

    def test_delete_content_when_delete_page(self):
        """Тест удаления контента при удалении страницы."""
        page_id = self.page.id
        content_id = self.content.id
        self.assertTrue(Page.objects.filter(id=page_id).exists())
        self.assertTrue(BaseContent.objects.filter(id=content_id).exists())
        self.page.delete()
        self.assertFalse(Page.objects.filter(id=page_id).exists())
        self.assertFalse(BaseContent.objects.filter(id=content_id).exists())

    def test_dont_delete_page_when_delete_content(self):
        """Тест удаления контента. При этом страница должна остаться."""
        page_id = self.page.id
        content_id = self.content.id
        self.assertTrue(Page.objects.filter(id=page_id).exists())
        self.assertTrue(BaseContent.objects.filter(id=content_id).exists())
        self.content.delete()
        self.assertTrue(Page.objects.filter(id=page_id).exists())
        self.assertFalse(BaseContent.objects.filter(id=content_id).exists())
