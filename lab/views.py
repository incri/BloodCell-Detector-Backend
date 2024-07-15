from django_filters.rest_framework import DjangoFilterBackend
import requests
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from core.models import User
from lab import filters
from . import models, serializers
from .pagination import DefaultPagination


class HospitalViewSet(ModelViewSet):
    serializer_class = serializers.HospitalSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "email"]
    ordering_fields = ["name"]
    filterset_fields = ["address"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Hospital.objects.all()
        else:
            hospitals = models.Hospital.objects.filter(id=user.hospital_id)
            return hospitals


class BloodTestViewSet(ModelViewSet):
    serializer_class = serializers.BloodTestSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.BloodTestFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.BloodTest.objects.prefetch_related("images").all()
        return models.BloodTest.objects.prefetch_related("images").filter(
            patient__hospital=user.hospital_id
        )

    def get_serializer_context(self):
        return {
            "patient_id": self.kwargs["patient_pk"],
            "request": self.request,
        }


class BloodTestImageDataViewSet(ModelViewSet):
    serializer_class = serializers.BloodTestImageDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        hospital_id = self.kwargs.get("hospital_pk")

        if user.is_superuser:
            return models.BloodTestImageData.objects.all()
        return models.BloodTestImageData.objects.filter(
            blood_test__patient__hospital=user.hospital_id
        )

    def get_serializer_context(self):
        return {
            "blood_test_id": self.kwargs["blood_tests_pk"],
            "request": self.request,
        }

    def create(self, request, *args, **kwargs):
        # Expecting files in request.FILES
        files = request.FILES.getlist("image")
        blood_test_id = self.kwargs["blood_tests_pk"]
        data = [{"image": file, "blood_test": blood_test_id} for file in files]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["post"], url_path="batch-delete")
    def batch_delete(self, request, *args, **kwargs):
        # Collect all image_ids from the request data
        image_ids = request.data.getlist("image_ids")
        if not image_ids:
            return Response(
                {"error": "No image IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        images = models.BloodTestImageData.objects.filter(id__in=image_ids)
        count, _ = images.delete()
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], url_path='images-for-bloodtest')
    def images_for_bloodtest(self, request, *args, **kwargs):
        bloodtest_id = request.data.get("bloodtest_id")
        if not bloodtest_id:
            return Response({"error": "Bloodtest ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch images associated with the blood test ID
            images = models.BloodTestImageData.objects.filter(blood_test_id=bloodtest_id)
        except models.BloodTestImageData.DoesNotExist:
            return Response({"error": "Blood test data not found"}, status=status.HTTP_404_NOT_FOUND)

        # Construct image URLs
        image_urls = [request.build_absolute_uri(image.image.url) for image in images]

        # Prepare data to send to FastAPI
        data = {
            'image_urls': ','.join(image_urls)  # Convert list to comma-separated string
        }

        # Print the format of image URLs being sent
        print(f"Sending image URLs to FastAPI: {data['image_urls']}")

        # URL of your FastAPI endpoint for processing images
        fastapi_url = 'http://127.0.0.1:7001/process-images/'

        try:
            # Send POST request to FastAPI
            response = requests.post(fastapi_url, data=data)  # Send data as form data

            # Check response status
            response.raise_for_status()
            
            # Parse FastAPI response
            fastapi_response = response.json()
            return Response(fastapi_response, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            error_message = f"Error sending images to FastAPI: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ResultImageDataViewSet(ModelViewSet):
    serializer_class = serializers.ResultImageDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.ResultImageData.objects.all()
        return models.ResultImageData.objects.filter(
            result__bloodtest__patient__hospital=user.hospital_id
        )

    def get_serializer_context(self):
        return {
            "result_id": self.kwargs["result_pk"],
            "request": self.request,
        }


class AddressViewSet(ModelViewSet):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Address.objects.all()
        return models.Address.objects.filter(patient__hospital=user.hospital_id)

    def get_serializer_context(self):
        return {
            "patient_id": self.kwargs["patient_pk"],
            "request": self.request,
        }


class PatientViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.PatientFilter
    pagination_class = DefaultPagination
    search_fields = ["first_name", "last_name", "phone"]
    ordering_fields = ["first_name"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Patient.objects.all()
        return models.Patient.objects.filter(hospital_id=user.hospital_id)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.PatientListSerializer
        if self.action == "retrieve":
            return serializers.PatientDetailSerializer
        return (
            serializers.PatientListSerializer
        )  # Fallback serializer to avoid AssertionError

    def get_serializer_context(self):
        return {
            "hospital_id": self.kwargs["hospital_pk"],
            "request": self.request,
        }


class ResultViewSet(ModelViewSet):
    serializer_class = serializers.ResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ResultFilter
    pagination_class = DefaultPagination
    search_fields = ["description"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Result.objects.all()
        return models.Result.objects.filter(
            bloodtest__patient__hospital=user.hospital_id
        )

    def get_serializer_context(self):
        return {
            "blood_test_id": self.kwargs["blood_tests_pk"],
            "request": self.request,
        }
