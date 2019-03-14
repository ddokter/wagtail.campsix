from rest_framework import viewsets, serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import SearchFilter, OrderingFilter
from wagtail.core.models import Page, PageRevision
from django_filters.rest_framework import DjangoFilterBackend
from .base import LinksModelSerializer, MetaMixin
from .pagination import LinksPagination
from .permissions import PagePermissions, can_publish_page, can_unpublish_page


class PageRevisionSerializer(LinksModelSerializer):

    class Meta:
        model = PageRevision
        fields = ('created_at',)


class PageSerializer(LinksModelSerializer):

    _type = serializers.SerializerMethodField(method_name="get_type")
    revisions = PageRevisionSerializer(many=True)

    def get_type(self, obj):

        return (obj.specific_class._meta.app_label + '.' +
                obj.specific_class.__name__)

    def get_links(self, obj):

        """ Add children link, if need be """

        _links = super(PageSerializer, self).get_links(obj)

        req = self.context.get('request')

        if obj.get_children().count():
            _links['children'] = reverse(
                "page-children",
                kwargs={'pk': obj.id},
                request=req)

        if can_publish_page(req.user, obj):
            _links['publish'] = reverse(
                "page-publish",
                kwargs={'pk': obj.id},
                request=req)

        if can_unpublish_page(req.user, obj):
            _links['unpublish'] = reverse(
                "page-unpublish",
                kwargs={'pk': obj.id},
                request=req)

        return _links

    class Meta:
        model = Page
        fields = ('_links', 'title', 'slug', '_type', 'live', 'expired',
                  'revisions')


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


class PageViewSet(MetaMixin, viewsets.ModelViewSet):

    """Wagtail CMS page listing. You can move into the page hierarchy by
    following the links provided by pages that have children.
    Search can be performed like this:

        /pages/?<meta.search.param>=about

    Filtering is allowed on the fields specified in <meta.filter.fields>, i.e.:

        /pages/?show_in_menus=True

    Currently, boolean filters take the pythonic string representation of
    true and false, e.g. True and False.

    Ordering may be performed on any field in <meta.ordering.fields.fields>,
    by using the parameter specified in <meta.ordering.param>. You can order
    according to natural ordering, or reverse.

        /pages/?<meta.ordering.param>=title,-slug

    """

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_class = PageFilter
    pagination_class = LinksPagination
    search_fields = ('title', 'slug',)
    filter_fields = ('title', 'show_in_menus')
    permission_classes = (PagePermissions,)

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

        context = {'request': self.request}

        serializer = PageTreeSerializer(qs, many=True, context=context)

        return Response(serializer.data)

    @detail_route()
    def publish(self, request, pk=None):

        page = self.get_object()

        rev = page.get_latest_revision()

        if not rev:
            rev = page.save_revision()

        rev.publish()

        serializer = self.get_serializer(page.get_latest_revision_as_page())

        return Response(serializer.data)

    @detail_route()
    def unpublish(self, request, pk=None):

        page = self.get_object()

        page.unpublish()

        serializer = self.get_serializer(page)

        return Response(serializer.data)
