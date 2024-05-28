from rest_framework import serializers
from . import models

class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = [
            "name",
            "address",
            "phone",
            "email",
            
        ]

