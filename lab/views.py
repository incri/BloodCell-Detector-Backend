from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models, serializers

class BloodTestViewSet(ModelViewSet):
    queryset = models.BloodTest.objects.all()
    serializer_class = serializers.BloodTestSerializer


class AddressViewSet(ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer

    def get_serializer_context(self):
        return {'patient_id': self.kwargs['patient_pk']}

class PatientViewSet(ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer

class ResultViewSet(ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer