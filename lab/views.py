from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import models, serializers
from . import filters
from .pagination import DefaultPagination


class BloodTestViewSet(ModelViewSet):
    queryset = models.BloodTest.objects.prefetch_related("images").all()
    serializer_class = serializers.BloodTestSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.BloodTestFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BloodTestImageDataViewSet(ModelViewSet):
    serializer_class = serializers.BloodTestImageDataSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return models.BloodTestImageData.objects.filter(
            blood_test_id=self.kwargs["blood_test_pk"]
        )

    def get_serializer_context(self):
        return {"blood_test_id": self.kwargs["blood_test_pk"]}


class ResultImageDataViewSet(ModelViewSet):
    serializer_class = serializers.ResultImageDataSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return models.ResultImageData.objects.filter(result=self.kwargs["result_pk"])

    def get_serializer_context(self):
        return {"result_id": self.kwargs["result_pk"]}


class AddressViewSet(ModelViewSet):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Address.objects.filter(patient_id=self.kwargs["patient_pk"])

    def get_serializer_context(self):
        return {"patient_id": self.kwargs["patient_pk"]}


class PatientViewSet(ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.PatientFilter
    pagination_class = DefaultPagination
    search_fields = ["first_name", "last_name", "phone"]
    ordering_fields = ["first_name"]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class ResultViewSet(ModelViewSet):
    serializer_class = serializers.ResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ResultFilter
    pagination_class = DefaultPagination
    search_fields = ["description"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return models.Result.objects.filter(bloodtest_id=self.kwargs["blood_test_pk"])

    def get_serializer_context(self):
        return {"blood_test_id": self.kwargs["blood_test_pk"]}
