from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers
from rest_framework.permissions import IsAdminUser

class HospitalViewSet(ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
    permission_classes = [IsAdminUser]
