from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from . import models, serializers
from . import filters

class BloodTestViewSet(ModelViewSet):
    queryset = models.BloodTest.objects.all()
    serializer_class = serializers.BloodTestSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.BloodTestFilter
    search_fields = ['title', 'description']




class AddressViewSet(ModelViewSet):
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        return models.Address.objects.filter(patient_id = self.kwargs['patient_pk'])

    def get_serializer_context(self):
        return {'patient_id': self.kwargs['patient_pk']}

class PatientViewSet(ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer

class ResultViewSet(ModelViewSet):
    serializer_class = serializers.ResultSerializer

    def get_queryset(self):
        return models.Result.objects.filter(bloodtest_id = self.kwargs['blood_test_pk'])


    def get_serializer_context(self):
        return {'blood_test_id': self.kwargs['blood_test_pk']}