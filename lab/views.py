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
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.core.files.base import ContentFile


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
        
        # Validate result_id
        if not result_id:
            return Response({"error": "result_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        hospital_id = self.kwargs.get("hospital_pk")

        return self.generate_pdf_response(hospital_id, result_id)

    def generate_pdf_response(self, hospital_id, result_id):
        hospital = get_object_or_404(models.Hospital, id=hospital_id)
        result = get_object_or_404(models.Result, id=result_id)
        blood_test = result.bloodtest
        patient = blood_test.patient
        result_images = models.ResultImageData.objects.filter(result=result)
        detections = models.LabResultDetection.objects.filter(result=result)
        non_zero_detections = [(detection.detection_type, detection.detection_value) for detection in detections if detection.detection_value > 0]


        # Create a BytesIO buffer to hold PDF data
        buffer = BytesIO()

        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Create a stylesheet for styling
        styles = getSampleStyleSheet()
        style_header = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=24, alignment=1, spaceAfter=12)
        style_section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=20, spaceAfter=6)
        style_section_content = ParagraphStyle('SectionContent', parent=styles['Normal'], fontSize=12, spaceAfter=6)
        style_footer = ParagraphStyle('Footer', parent=styles['Heading1'], fontSize=18, alignment=1, spaceBefore=40, borderTop='1px solid #cccccc', spaceAfter=12)

        # Content list
        content = []

        # Header
        content.append(Paragraph(hospital.name, style_header))
        content.append(Paragraph(hospital.address, styles['Normal']))
        content.append(Paragraph(f"Phone: {hospital.phone}", styles['Normal']))
        content.append(Paragraph(f"Email: {hospital.email}", styles['Normal']))
        content.append(Spacer(1, 12))

        # Patient Information
        content.append(Paragraph("Patient Information", style_section_heading))
        patient_info = [
            [f"Name:", f"{patient.first_name} {patient.last_name}"],
            [f"Email:", f"{patient.email}"],
            [f"Phone:", f"{patient.phone}"],
            [f"Birth Date:", f"{patient.birth_date}"]
        ]
        table = Table(patient_info, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Blood Test Information
        content.append(Paragraph("Test Details", style_section_heading))
        blood_test_info = [
            [f"", blood_test.title],
            [f"", blood_test.description],
            [f"Registered At:", blood_test.created_at],
        ]
        table = Table(blood_test_info, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Result Information
        result_info = [
            [f"Summary:", result.description],
        ]
        table = Table(result_info, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

         # Detection Information
        detection_info = [['Cells Type', 'Value']] + [[detection_type, detection_value] for detection_type, detection_value in non_zero_detections]
        if detection_info:
            detection_table = Table(detection_info, colWidths=[2*inch, 2.5*inch])
            detection_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Add box around table
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines inside table
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray)  # Background for header row
            ]))
            content.append(detection_table)
        else:
            content.append(Paragraph("No detection information available.", styles['Normal']))
        content.append(Spacer(1, 12))

        # Result Images (3 images per row with spacing)
        image_table_data = []
        row = []
        for i, img in enumerate(result_images):
            img_file = img.image
            if isinstance(img_file, str):  # Handle file path
                try:
                    image = Image(img_file, width=2*inch, height=2*inch)
                except Exception as e:
                    print(f"Error loading image {img_file}: {e}")
                    continue
            elif hasattr(img_file, 'read'):  # Handle file-like object
                image = Image(BytesIO(img_file.read()), width=2*inch, height=2*inch)
            else:
                continue
            
            # Append images to rows, 3 per row
            if i % 3 == 0 and row:
                image_table_data.append(row)
                row = []
            row.append(image)
        
        if row:
            image_table_data.append(row)

        if image_table_data:
            image_table = Table(image_table_data, colWidths=[2*inch]*3, rowHeights=[2*inch]*len(image_table_data))  # 3 columns
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            content.append(image_table)
        
        # Footer
        content.append(Spacer(1, 12))
        content.append(Paragraph("End of Report", style_footer))

        # Build the PDF
        doc.build(content)

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

        channel_layer = get_channel_layer()

        def send_progress(message):
            print("reached")
            async_to_sync(channel_layer.group_send)(
                'progress_group',
                {
                    'type': 'progress_message',
                    'message': message
                }
            )

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
            'image_urls': ','.join(image_urls)
        }

        send_progress("Sending request to blood cell count API")

        # URL of your FastAPI endpoints
        blood_count_api_url = 'http://127.0.0.1:7001/process-images/'
        cell_type_api_url = 'http://127.0.0.1:7001/process-blood-types-images/'

        try:
            # Send POST request to blood cell count FastAPI
            response_blood_count = requests.post(blood_count_api_url, data=data)
            response_blood_count.raise_for_status()
            blood_count_response = response_blood_count.json()
            blood_count = blood_count_response["detected"]

            send_progress("Received response from blood cell count API")

            # Prepare data for the second FastAPI request
            data['processed_images'] = ','.join(blood_count_response['processed_images'])

            send_progress("Sending request to red blood cell type count API")

            # Send POST request to cell type count FastAPI
            response_cell_type = requests.post(cell_type_api_url, data=data)
            response_cell_type.raise_for_status()
            cell_type_response = response_cell_type.json()
            cell_type = cell_type_response["detected"]

            send_progress("Received response from red blood cell type count API")

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Create a new LabResult instance
                result = models.Result.objects.create(
                    description="Summary of the blood test results",
                    bloodtest_id=bloodtest_id
                )

                # Save the processed image links from both responses
                processed_images = blood_count_response['processed_images'] + cell_type_response['processed_images']
                for image_url in processed_images:
                    models.ResultImageData.objects.create(result=result, image=image_url)

                # Save detection results in LabResultDetection
                detections = {**blood_count, **cell_type}  # Combine both detection dictionaries
                for detection_type, detection_value in detections.items():
                    models.LabResultDetection.objects.create(
                        result=result,
                        detection_type=detection_type,
                        detection_value=detection_value
                    )

                send_progress("Processing complete")

                return Response({"message": "Data stored successfully"}, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            error_message = f"Error sending images to FastAPI: {str(e)}"
            send_progress(error_message)
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            send_progress(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            send_progress(error_message)
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
    
    def create(self, request, *args, **kwargs):
        # Extract patient data from the request
        patient_data = request.data

        # Validate and create the patient instance
        serializer = self.get_serializer(data=patient_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Automatically create an empty Address instance for the patient
        models.Address.objects.create(patient=serializer.instance)

        # Prepare the response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


