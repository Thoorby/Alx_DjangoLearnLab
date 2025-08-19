from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read: anyone
    Write: only the object author/owner
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj has 'author' in both Post and Comment
        return getattr(obj, 'author', None) == request.user
