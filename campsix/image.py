from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from wagtail.images.models import Image
from django_filters.rest_framework import DjangoFilterBackend
from .base import LinksModelSerializer, MetaMixin
from .pagination import LinksPagination


class ImageSerializer(LinksModelSerializer):

    def get_links(self, obj):

        """ Add children link, if need be """

        _links = super().get_links(obj)

        return _links

    class Meta:
        model = Image
        fields = ('_links', 'title', 'file', 'width', 'height', 'created_at')


class ImageSummarySerializer(ImageSerializer):

    pass


class ImageViewSet(MetaMixin, viewsets.ModelViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = LinksPagination
    search_fields = ('title',)
    filter_fields = ('title',)
