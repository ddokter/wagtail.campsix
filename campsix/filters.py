from django_filters import rest_framework as filters
from django_filters import BooleanFilter
from wagtail.core.models import Page


class InFilterMixin(object):

    def in_filter(self, queryset, name, value):

        _filter = {"%s__in" % name: self.request.query_params.getlist(name)}

        return queryset.filter(**_filter)


class PageFilter(filters.FilterSet, InFilterMixin):

    show_in_menus = BooleanFilter(field_name='show_in_menus')
    # id = NumberFilter(method='in_filter')

    class Meta:
        model = Page
        fields = ('show_in_menus',)
