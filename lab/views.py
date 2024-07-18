from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.template.loader import get_template

from rest_framework.exceptions import ValidationError
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

from io import BytesIO
from xhtml2pdf import pisa

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
            "blood_test_id": self.kwargs.get("blood_tests_pk"),
            "request": self.request,
        }
    
    @action(detail=True, methods=["get"], url_path="generate-report")
    def generate_report(self, request, *args, **kwargs):
        result_id = request.query_params.get('result_id')
        # Now you can use result_id to fetch the relevant data and generate your report


        # Optional: Validate result_id if required
        if not result_id:
            return Response({"error": "result_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        hospital_id = self.kwargs.get("hospital_pk")
        print(hospital_id)

        return self.generate_pdf_response(hospital_id, result_id)

    def generate_pdf_response(self, hospital_id, result_id):
        hospital = get_object_or_404(models.Hospital, id=hospital_id)
        result = get_object_or_404(models.Result, id=result_id)
        blood_test = result.bloodtest
        patient = blood_test.patient
        result_images = models.ResultImageData.objects.filter(result=result)

        # print(result_images)

        # Prepare data for rendering HTML template
        context = {
            'hospital': hospital,
            'patient': patient,
            'blood_test': blood_test,
            'result': result,
            'result_images' : result_images,
        }

        try:
            # Render HTML content from template
            template = get_template('report_template.html')
            html_content = template.render(context)
        except TemplateDoesNotExist:
            return Response('Template not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f'Error rendering template: {str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create a BytesIO buffer to hold PDF data
        buffer = BytesIO()

        # Use pisa to convert HTML to PDF
        try:
            pisa_status = pisa.CreatePDF(
                html_content.encode('UTF-8'),  # Ensure HTML content is encoded properly
                dest=buffer
            )
            if pisa_status.err:
                return Response('Failed to generate PDF', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f'Error generating PDF: {str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get the value of the BytesIO buffer and create the HttpResponse
        pdf_data = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{patient.first_name}_{patient.last_name}_report.pdf"'
        return response

class BloodTestImageDataViewSet(ModelViewSet):
    serializer_class = serializers.BloodTestImageDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

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
            'bloodtest_id': bloodtest_id,
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

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Save the results into the Django models
                result_data = {
                    'description': (
                        f"RBC Count: {fastapi_response['rbc_count']}, "
                        f"WBC Count: {fastapi_response['wbc_count']}, "
                        f"Platelets Count: {fastapi_response['platelets_count']}"
                    ),
                    'bloodtest': bloodtest_id  # Ensure bloodtest_id is correctly passed here
                }
                result_serializer = serializers.ResultSerializer(data=result_data, context={'request': request, 'blood_test_id': bloodtest_id})
                if result_serializer.is_valid():
                    result = result_serializer.save()

                    # Save the processed image links
                    for image_url in fastapi_response['processed_images']:
                        image_data = {
                            'result': result.id,  # Ensure result.id is correctly set
                            'image': image_url  # Use image_url field
                        }
                        image_serializer = serializers.ResultImageDataSerializer(data=image_data, context={'request': request, 'result_id': result.id})  # Pass result_id here
                        if image_serializer.is_valid():
                            image_serializer.save()
                        else:
                            raise ValidationError(image_serializer.errors)  # Raise ValidationError

                    return Response(result_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError(result_serializer.errors)  # Raise ValidationError

        except requests.exceptions.RequestException as e:
            error_message = f"Error sending images to FastAPI: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





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


