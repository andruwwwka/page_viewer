"""Описание админских интерфейсов."""
from django.contrib import admin

from .models import AudioContent, Page, TextContent, VideoContent


class BaseContentInlineAdmin(admin.TabularInline):
    """Базовый класс для инлайн элементов контента."""

    extra = 1
    exclude = ('counter',)


class AudioContentInlineAdmin(BaseContentInlineAdmin):
    """Инлайн класс для аудио контента."""

    model = AudioContent


class TextContentInlineAdmin(BaseContentInlineAdmin):
    """Инлайн класс для текстового контента."""

    model = TextContent


class VideoContentInlineAdmin(BaseContentInlineAdmin):
    """ИНлайн класс для видео контента."""

    model = VideoContent


class PageAdmin(admin.ModelAdmin):
    """Админский интерфейс страниц."""

    search_fields = (
        'title',
        'items__title',
    )
    inlines = (
        AudioContentInlineAdmin,
        TextContentInlineAdmin,
        VideoContentInlineAdmin,
    )


admin.site.register(Page, PageAdmin)
