from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from . import models, serializers
from . import filters
from .pagination import DefaultPagination


class BloodTestViewSet(ModelViewSet):
    queryset = models.BloodTest.objects.prefetch_related("images","results").all()
    serializer_class = serializers.BloodTestSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.BloodTestFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]

class BloodTestImageDataViewSet(ModelViewSet):
    serializer_class = serializers.BloodTestImageDataSerializer
    
    def get_queryset(self):
        return models.BloodTestImageData.objects.filter(blood_test_id=self.kwargs["blood_test_pk"])
    
    def get_serializer_context(self):
        return {"blood_test_id": self.kwargs["blood_test_pk"]}


class ResultImageDataViewSet(ModelViewSet):
    serializer_class = serializers.ResultImageDataSerializer
    
    def get_queryset(self):
        return models.ResultImageData.objects.filter(result=self.kwargs["result_pk"])
    
    def get_serializer_context(self):
        return {"result_id": self.kwargs["result_pk"]}



class AddressViewSet(ModelViewSet):
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        return models.Address.objects.filter(patient_id=self.kwargs["patient_pk"])

    def get_serializer_context(self):
        return {"patient_id": self.kwargs["patient_pk"]}


class PatientViewSet(ModelViewSet):
    queryset = models.Patient.objects.prefetch_related("blood_tests").all()
    serializer_class = serializers.PatientSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.PatientFilter
    pagination_class = DefaultPagination
    search_fields = ["first_name", "last_name", "phone"]
    ordering_fields = ["first_name"]


class ResultViewSet(ModelViewSet):
    serializer_class = serializers.ResultSerializer

    def get_queryset(self):
        return models.Result.objects.prefetch_related("result_images").filter(bloodtest_id=self.kwargs["blood_test_pk"])

    def get_serializer_context(self):
        return {"blood_test_id": self.kwargs["blood_test_pk"]}

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ResultFilter
    pagination_class = DefaultPagination
    search_fields = ["description"]
    ordering_fields = ["created_at"]

