from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Allows only the subscriber to receive the article
        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in SAFE_METHODS:
            if request.user.groups.filter(name='subscribers').exists() or obj.is_public:
                return True
        return obj.author == request.user and request.user.groups.filter(name='author').exists()


class IsSubscriberOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        Allows unauthorized users to get public articles and make articles only to authors
        :param request:
        :param view:
        :return:
        """
        if request.method in SAFE_METHODS:
            return True
        elif request.user and request.user.is_authenticated \
                and request.user.groups.filter(name='authors').exists() \
                or request.user.is_superuser:
            return True
