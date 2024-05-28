from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff



class HospitalUserCreationPermission(permissions.BasePermission):
    """
    Permission to control user creation based on the role of the creator.
    """

    def has_permission(self, request, view):
        # Check if the requesting user is authenticated
        if request.user.is_authenticated:
            # Check if the requesting user is a superuser
            if request.user.is_superuser:
                return True
            # Check if the requesting user is a hospital admin
            elif hasattr(request.user, 'is_hospital_admin') and request.user.is_hospital_admin:
                # If the user is a hospital admin, ensure they can only create users for their own hospital
                hospital_id = request.user.hospital_id
                if 'hospital' in request.data:
                    # If the request includes a hospital field, ensure it matches the admin's hospital
                    return str(request.data['hospital']) == str(hospital_id)
                else:
                    # If no hospital field is provided, default to the admin's hospital
                    return True
        # If the user is not authenticated or is not a hospital admin, deny permission
        return False
