from rest_framework import permissions


def can_publish_page(user, page):

    return not page.live and (user == page.owner or user.is_superuser)


def can_unpublish_page(user, page):

    return page.live and (user == page.owner or user.is_superuser)


class PagePermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if obj.live:
            if request.method in permissions.SAFE_METHODS:
                return True

        return obj.owner == request.user or request.user.is_superuser
