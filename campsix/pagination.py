from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse


class LinksPagination(PageNumberPagination):

    """ Custom implementation for pagination to allow for next and previous
    links in the _links field """

    max_page_size = 100
    page_size = 4

    def get_paginated_response(self, data):

        _links = {}

        if self.page.has_next():
            _links['next'] = self.get_next_link()

        if self.page.has_previous():
            _links['previous'] = self.get_previous_link()

        current = self.page.number
        final = self.page.paginator.num_pages

        params = ""

        for item in self.request.query_params.items():
            if item[0] != "page":
                params += "%s=%s&" % item

        _links['self'] = "%s?page=%i" % (reverse(
            "page-list",
            request=self.request), current)

        for num in range(1, final):
            if num is not None:
                _links[num] = "%s?%spage=%i" % (reverse(
                    "page-list",
                    request=self.request), params, num)

        return Response({
            '_links': _links,
            'count': self.page.paginator.count,
            'current': current,
            'results': data
        })
