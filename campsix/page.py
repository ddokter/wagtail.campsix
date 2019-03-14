from rest_framework import viewsets, serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import SearchFilter, OrderingFilter
from wagtail.core.models import Page
from django_filters.rest_framework import DjangoFilterBackend
from .base import LinksModelSerializer
from .pagination import LinksPagination
from .filters import PageFilter


class PageSerializer(LinksModelSerializer):

    _type = serializers.SerializerMethodField(method_name="get_type")

    def get_type(self, obj):

        return (obj.specific_class._meta.app_label + '.' +
                obj.specific_class.__name__)

    def get_links(self, obj):

        """ Add children link, if need be """

        _links = super(PageSerializer, self).get_links(obj)

        if obj.get_children().count():
            _links['children'] = reverse(
                "page-children",
                kwargs={'pk': obj.id},
                request=self.context.get('request'))

        return _links

    class Meta:
        model = Page
        fields = ('_links', 'title', 'slug', '_type')


class PageSummarySerializer(PageSerializer):

    pass


class PageTreeSerializer(PageSerializer):

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return PageTreeSerializer(
            obj.get_children(),
            many=True).data

    class Meta:
        model = Page
        fields = ('_links', 'title', 'slug', '_type', 'children')


class PageViewSet(viewsets.ModelViewSet):

    """Wagtail CMS page listing. You can move into the page hierarchy by
    following the links provided by pages that have children.
    Search can be performed like this:

        /pages/?search=about

    Search fields are title and slug.

    Filtering is allowed on the fields:

      * show_in_menus

    To use a specific filter, add it to the URL:

        /pages/?show_in_menus=True

    Currently, this filter takes the pythonic string representation of
    true and false, e.g. True and False.

    """

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = PageFilter
    pagination_class = LinksPagination
    search_fields = ('title', 'slug',)

    @detail_route()
    def children(self, request, pk=None):

        qs = self.get_object().get_children()

        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @list_route()
    def tree(self, request):

        qs = Page.objects.all()

        qs = [page for page in qs if page.is_root()]

        serializer = PageTreeSerializer(qs, many=True)

        return Response(serializer.data)
