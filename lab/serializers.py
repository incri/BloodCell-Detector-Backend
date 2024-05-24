from rest_framework import serializers
from . import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = [
            "id",
            "street",
            "city",
        ]

    def create(self, validated_data):
        patient_id = self.context["patient_id"]
        return models.Address.objects.create(patient_id=patient_id, **validated_data)


class BloodTestImageDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.BloodTestImageData
        fields = ["id", "image",]

 
    def create(self, validated_data):
        blood_test_id = self.context["blood_test_id"]
        return models.BloodTestImageData.objects.create(
            blood_test_id=blood_test_id, **validated_data
        )

class ResultImageDataSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        result_id = self.context["result_id"]
        return models.ResultImageData.objects.create(
            result_id=result_id, **validated_data
        )
    
    class Meta:
        model = models.ResultImageData
        fields = ["id", "image",]


class ResultSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    result_images = ResultImageDataSerializer(many=True, read_only=True)

    class Meta:
        model = models.Result
        fields = ["id", "created_at", "description", "result_images"]

    def create(self, validated_data):
        blood_test_id = self.context["blood_test_id"]
        return models.Result.objects.create(
            bloodtest_id=blood_test_id, **validated_data
        )




class BloodTestSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    images = BloodTestImageDataSerializer(many = True, read_only = True)

    results = ResultSerializer(many=True, read_only=True)


    class Meta:
        model = models.BloodTest
        fields = ["id", "title", "description", "patient", "images", "results"]



class PatientSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    blood_tests = BloodTestSerializer(many = True, read_only = True)
    address = AddressSerializer(read_only = True)


    class Meta:
        model = models.Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "address",
            "blood_tests",
        ]


