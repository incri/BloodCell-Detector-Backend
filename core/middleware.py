from django.core.exceptions import PermissionDenied
from django.urls import resolve
from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
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
            if hospital_id and str(hospital_id) != str(user.hospital_id):
                raise PermissionDenied("User cannot access data from this hospital")

            return self.get_response(request)

        except AuthenticationFailed:
            # Handle invalid or expired token error with JSON response
            return JsonResponse({"detail": "Invalid or expired token."}, status=401)

        except PermissionDenied as e:
            # Handle permission denied error with JSON response
            return JsonResponse({"detail": str(e)}, status=403)
