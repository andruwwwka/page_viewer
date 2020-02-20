"""Описание ресурсов API страниц."""
from rest_framework import fields, mixins, serializers
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from ..models import Page
from ..tasks import increment_counter

__all__ = ('PageView', )


class ContentItemSerializer(serializers.ModelSerializer):
    """Общий сериализатор для всех типов контента."""

    class Meta:  # noqa D106
        exclude = ('id', 'page')

    def __init__(self, instance=None, *args, **kwargs):
        self.Meta.model = type(instance)
        super(ContentItemSerializer, self).__init__(instance, *args, **kwargs)


class ItemRelatedField(serializers.RelatedField):
    """Поле для элементов контента на странице."""

    available_types_of_content = ('audiocontent', 'textcontent', 'videocontent')

    def to_representation(self, obj):
        """Метод сериализации элемента контента."""
        serializer = None
        for type_of_content in self.available_types_of_content:
            if hasattr(obj, type_of_content):
                serializer = ContentItemSerializer(getattr(obj, type_of_content))
        if serializer is None:
            raise RuntimeError(f'Missing type of content for {obj}')
        return serializer.data


class DetailPageSerializer(serializers.ModelSerializer):
    """Сериалайзер для детального отображения страницы."""

    items = ItemRelatedField(read_only=True, many=True)

    class Meta:  # noqa D106
        model = Page
        fields = ('title', 'items')


class ListPageSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения списка страниц."""

    page_url = fields.SerializerMethodField()

    class Meta:  # noqa D106
        model = Page
        fields = ('page_url', 'title')

    def get_page_url(self, obj):
        """Получение относительной ссылки на страницу."""
        return reverse('pages-detail', args=(obj.id, ))


class PageView(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    """Представление для ресурса страниц."""

    queryset = Page.objects.all()
    available_serializers = {
        'list': ListPageSerializer,
        'retrieve': DetailPageSerializer,
    }

    def retrieve(self, request, *args, **kwargs):
        """Метод получения данных о странице.

        Вызывается задача инкремента счетчика просмотров контента.
        """
        increment_counter.delay(kwargs['pk'])
        return super(PageView, self).retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор класса сериалайзера в зависимости от метода обращения к API."""
        if self.action not in self.available_serializers:
            raise RuntimeError(f'Action {self.action} does not supported')
        serializer_class = self.available_serializers[self.action]
        return serializer_class
