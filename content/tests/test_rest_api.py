"""Тесты на API приложения."""
from django.test import override_settings
from django.test.testcases import TestCase
from django.urls import reverse

from ..models import AudioContent, Page, TextContent, VideoContent


class TestRestApi(TestCase):
    """Тесты API."""

    def setUp(self):
        """Подготовка тестовых данных."""
        super().setUp()
        self.page_with_audio_item = Page.objects.create(title='Page with audio content')
        self.page_with_text_item = Page.objects.create(title='Page with text content')
        self.page_with_video_item = Page.objects.create(title='Page with video content')
        self.audio_content = AudioContent.objects.create(
            title='Audio content',
            bitrate=256,
            page=self.page_with_audio_item,
        )
        TextContent.objects.create(
            title='Text content',
            body='Text body',
            page=self.page_with_text_item,
        )
        VideoContent.objects.create(
            title='Video content',
            video_file='http://test.com',
            page=self.page_with_video_item,
        )

    def test_pages_list_format(self):
        """Тест формата списка страниц."""
        response = self.client.get(reverse('pages-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(all((attr in response_data for attr in ['count', 'next', 'previous', 'results'])))
        result_item = response_data['results'][0]
        self.assertTrue(all((attr in result_item for attr in ['page_url', 'title'])))

    def test_page_detail_format(self):
        """Тест формата детальной информации о странице."""
        page = Page.objects.first()
        response = self.client.get(reverse('pages-detail', kwargs={'pk': page.id}))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(all((attr in response_data for attr in ['title', 'items'])))
        item = response_data['items'][0]
        self.assertTrue(all((attr in item for attr in ['title', 'order', 'counter'])))

    def test_audio_item_format(self):
        """Тест формата аудио контента."""
        response = self.client.get(reverse('pages-detail', kwargs={'pk': self.page_with_audio_item.id}))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        item = response_data['items'][0]
        self.assertTrue(all((attr in item for attr in ['title', 'order', 'counter', 'bitrate'])))

    def test_text_item_format(self):
        """Тест формата текстового контента."""
        response = self.client.get(reverse('pages-detail', kwargs={'pk': self.page_with_text_item.id}))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        item = response_data['items'][0]
        self.assertTrue(all((attr in item for attr in ['title', 'order', 'counter', 'body'])))

    def test_video_item_format(self):
        """Тест формата видео контента."""
        response = self.client.get(reverse('pages-detail', kwargs={'pk': self.page_with_video_item.id}))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        item = response_data['items'][0]
        self.assertTrue(all((attr in item for attr in ['title', 'order', 'counter', 'video_file', 'subs'])))

    @override_settings(task_always_eager=True)
    def test_increment_counter(self):
        """Тест инкремента счетчика просмотра контента."""
        counter_before_request = self.audio_content.counter
        response = self.client.get(reverse('pages-detail', kwargs={'pk': self.page_with_audio_item.id}))
        self.assertEqual(response.status_code, 200)
        self.audio_content.refresh_from_db()
        self.assertEqual(self.audio_content.counter, counter_before_request + 1)

    def test_pagination(self):
        """Тест постраничного отображения."""
        first_page_response = self.client.get(reverse('pages-list'))
        self.assertEqual(first_page_response.status_code, 200)
        first_page_response_data = first_page_response.json()
        self.assertEqual(len(first_page_response_data['results']), 10)
        self.assertIsNotNone(first_page_response_data['next'])
        self.assertIsNone(first_page_response_data['previous'])
        second_page_response = self.client.get(reverse('pages-list'), data={'page': 2})
        self.assertEqual(second_page_response.status_code, 200)
        second_page_response_data = second_page_response.json()
        self.assertEqual(len(second_page_response_data['results']), Page.objects.count() - 10)
        self.assertIsNone(second_page_response_data['next'])
        self.assertIsNotNone(second_page_response_data['previous'])

    def test_per_page(self):
        """Тест переопределения количества элементов на странице."""
        three_on_page_response = self.client.get(reverse('pages-list'), data={'per_page': 3})
        self.assertEqual(three_on_page_response.status_code, 200)
        three_on_page_response_data = three_on_page_response.json()
        self.assertEqual(len(three_on_page_response_data['results']), 3)
        five_on_page_response = self.client.get(reverse('pages-list'), data={'per_page': 5})
        self.assertEqual(five_on_page_response.status_code, 200)
        five_on_page_response_data = five_on_page_response.json()
        self.assertEqual(len(five_on_page_response_data['results']), 5)

    def test_404_on_not_exists_page(self):
        """Тест обращения к несуществующей странице."""
        not_exists_page_id = Page.objects.latest('id').id + 1
        response = self.client.get(reverse('pages-detail', kwargs={'pk': not_exists_page_id}))
        self.assertEqual(response.status_code, 404)

    def test_404_on_not_exists_page_of_pages(self):
        """Тест обращения к несуществующей странице (странице пагинации)."""
        page = Page.objects.count() // 10 + 2
        response = self.client.get(reverse('pages-list'), data={'page': page})
        self.assertEqual(response.status_code, 404)
