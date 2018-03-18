from rest_framework import permissions
from .models import Store

class OrderApiPermissions(permissions.BasePermission):
    """
    Custom permission that guarantee that only staff members of the store owning the order have the right to access it  .
    """

    def has_object_permission(self, request, view, obj):
        return str(request.user) in obj.store.get_staff()

    def has_permission(self, request, view):

        store_id = request.resolver_match.kwargs.get('store_id')
        store = Store.objects.get(id=store_id)

        return str(request.user) in store.get_staff()


class StoreApiPermissions(permissions.BasePermission):
    # TODO : to improve
    """
    Custom permission that guarantee that only staff members of the store have the right to access it  .
    """

    def has_object_permission(self, request, view, obj):

        return str(request.user.get_store().pk) == request.resolver_match.kwargs.get('pk')




class CourierApiPermissions(permissions.BasePermission):
    """
    Custom permission that guarantee that only staff members of the store owning the order have the right to access it  .
    """
    #TODO: To improve

    def has_object_permission(self, request, view, obj):
        return obj.code in request.user.get_store().get_couriers()


