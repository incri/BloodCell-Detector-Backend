from rest_framework import serializers
from . import models

class BloodTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.BloodTest
        fields = ['id', 'title', 'description', 'detection']
    

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id', 'street', 'city',]

    def create(self, validated_data):
        patient_id = self.context['patient_id']
        return models.Address.objects.create(patient_id = patient_id, **validated_data)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ['id', 'created_at', 'description', 'blood_test' ]