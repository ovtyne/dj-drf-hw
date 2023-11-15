from rest_framework.permissions import BasePermission

from lms.models import Subscription
from users.models import UserRoles


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRoles.MEMBER:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True


class IsSubscriber(BasePermission):

    def has_object_permission(self, request, view, obj):
        if Subscription.objects.filter(user=request.user, course=obj):
            return True
