from django.urls import path, include
from rest_framework import routers
from .page import PageViewSet


class WagtailAPIRootView(routers.APIRootView):

    """Wagtail API root. Root level resources are shown. Use provided
    links to gain access to the resources that are published by the
    API and find out what there is to see. The API is set up following
    the principles of HATEOAS, so what you see is what you can...

    """

    def get(self, request, *args, **kwargs):

        """ Override root view to add the auth views, like so:

            self.api_root_dict["foo"] = "foo"

        """

        return super(WagtailAPIRootView, self).get(request, *args, **kwargs)


class WagtailRouter(routers.DefaultRouter):

    APIRootView = WagtailAPIRootView

    def get_urls(self):

        urls = super(WagtailRouter, self).get_urls()

        return urls


router = WagtailRouter()


router.register(r'pages', PageViewSet)


urlpatterns = [
    path(r'', include(router.urls))
]
