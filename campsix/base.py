from rest_framework import serializers, fields
from rest_framework.reverse import reverse


class AllowedMethodsMixin(object):

    """List CRUD methods for given object. This is handy in case the
    model that is serialized is embedded, but the client needs to know
    what methods are allowed on the object. This makes it unnecessary
    to call each separate object from the client to discover allowed
    methods.

    """

    def get_allowed_methods(self, obj):

        request = self.context['request']

        if not request.user.is_authenticated and hasattr(request, 'role'):
            return []

        allowed = ["OPTIONS"]

        model_perms = request.role.rights.permissions_for_model(
            getattr(self.Meta, 'model'))

        if model_perms.read(obj):
            allowed.append('GET')

        if model_perms.update(obj):
            allowed.append('PUT')
            allowed.append('PATCH')

        if model_perms.delete(obj):
            allowed.append('DELETE')

        return allowed


class LinksMixin(object):

    """Serializer base class that adds the links field to the resource"""

    _links = serializers.SerializerMethodField(method_name="get_links")

    def absolutize(self, path):

        return self.context['request'].build_absolute_uri(path)

    def get_links(self, obj):

        detail_viewname = getattr(
            self, "detail_view",
            "%s-detail" % (obj.__class__.__name__.lower()))

        links = {}

        try:
            links['self'] = reverse(
                detail_viewname,
                kwargs={'pk': obj.id},
                request=self.context.get('request'))
        except:
            try:
                links['self'] = reverse(
                    detail_viewname,
                    kwargs={'slug': obj.slug},
                    request=self.context.get('request'))
            except:
                pass

        try:
            parent = obj.get_parent()

            parent_viewname = "%s-detail" % parent.__class__.__name__.lower()

            links['parent'] = reverse(
                parent_viewname,
                kwargs={'pk': parent.id},
                request=self.context.get('request'))
        except:
            """ Looks like we do not have a parent. No worries.
            Who needs 'em """

        return links


class LinksModelSerializer(LinksMixin, serializers.ModelSerializer):

    _links = serializers.SerializerMethodField(method_name="get_links")


class AbsoluteURLField(fields.CharField):

    def to_representation(self, value):
        return self.context['request'].build_absolute_uri(value)


class MetaMixin(object):

    def list(self, request, *args, **kwargs):

        """ Override list method so as to be able to add filtering meta info
        """

        response = super().list(request)

        meta = {}

        for _filter in self.filter_backends:
            if hasattr(_filter, 'ordering_param'):
                meta['ordering'] = {
                    'param': _filter.ordering_param,
                    'fields': [pair[0] for pair in
                               _filter().get_valid_fields(self.queryset, self)]
                    }
            elif hasattr(_filter, 'search_param'):
                meta['search'] = {
                    'param': _filter.search_param
                    }
            elif hasattr(_filter, 'get_filter_class'):

                _ffilter = _filter().get_filter_class(self, self.queryset)()

                meta['filter'] = {'fields': {}}

                for (name, _type) in _ffilter.get_filters().items():
                    meta['filter']['fields'][name] = _type.__class__.__name__

        response.data['meta'] = meta

        return response
