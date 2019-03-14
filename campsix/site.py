from rest_framework.views import APIView
from .page import PageViewSet


class Tree(APIView):

    def get(self, request, format=None):

        func = PageViewSet.tree

        return func(self, request)
