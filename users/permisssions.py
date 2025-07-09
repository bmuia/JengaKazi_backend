from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    """
    Custom permission to only allow employers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'
