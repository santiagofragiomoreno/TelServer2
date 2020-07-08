from rest_framework.permissions import BasePermission


class IsIot(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        for group in request.user.groups.all():
            if group.name == 'IoT':
                return True
        return False


class IsClient(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        for group in request.user.groups.all():
            if group.name == 'Client':
                return True
        return False


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        for group in request.user.groups.all():
            if group.name == 'Owner':
                return True
        return False


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        for group in request.user.groups.all():
            if group.name == 'Superuser':
                return True
        return False