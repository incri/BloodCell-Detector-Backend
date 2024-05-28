from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from .models import Hospital
from .serializers import HospitalSerializer

User = get_user_model()


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAdminUser]