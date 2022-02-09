from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user.groups.filter(name='subscribers').exists() or obj.is_public:
                return True

        return obj.author == request.user


class IsSubscriberOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            elif request.user.groups.filter(name='authors').exists():
                return True
