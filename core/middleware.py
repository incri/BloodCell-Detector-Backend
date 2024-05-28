

from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied

class HospitalAccessMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if not user.is_authenticated:
            return None

        if user.is_superuser:
            return None

        # Get the hospital id from the user's profile
        hospital_id = getattr(user, 'hospital_id', None)
        if hospital_id is None:
            raise PermissionDenied("User does not belong to any hospital")

        # Restrict access to the hospital data
        if 'hospital_id' in request.resolver_match.kwargs:
            if request.resolver_match.kwargs['hospital_id'] != str(hospital_id):
                raise PermissionDenied("User cannot access data from this hospital")

        return None
