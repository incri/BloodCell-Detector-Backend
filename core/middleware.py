from django.core.exceptions import PermissionDenied
from django.urls import resolve



from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        drf_request: RestFrameworkRequest = APIView().initialize_request(request)
        user = drf_request.user
        resolver_match = resolve(request.path_info)
        hospital_id = resolver_match.kwargs.get('hospital_pk')


        # Allow access if user is not authenticated
        if not user.is_authenticated:
            return self.get_response(request)

        # Allow access for superusers
        if user.is_superuser:
            return self.get_response(request)

        # Retrieve hospital ID from user profile
        if user.hospital_id is None:
            raise PermissionDenied("User does not belong to any hospital")
        
        # Check if the requested hospital ID matches the user's hospital ID
        if hospital_id:
            if str(hospital_id) != str(user.hospital_id):
                raise PermissionDenied("User cannot access data from this hospital")


        # this will work while sending reponse
        return self.get_response(request)
        