from rest_framework import serializers
from . import models


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "email",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = [
            "id",
            "street",
            "city",
            "patient",
        ]

    def create(self, validated_data):
        patient_id = self.context["patient_id"]
        user_hospital_id = self.context["request"].user.hospital.id
        patient_hospital_id = validated_data["patient"].hospital.id

        if str(patient_hospital_id) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create data for patients from other hospitals."
            )

        return models.Address.objects.create(patient_id=patient_id, **validated_data)


class BloodTestImageDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BloodTestImageData
        fields = [
            "id",
            "image",
            "blood_test",
        ]

    def create(self, validated_data):
        blood_test_id = self.context["blood_test_id"]
        user_hospital_id = self.context["request"].user.hospital.id
        blood_test_hospital = validated_data["blood_test"].patient.hospital.id

        if str(blood_test_hospital) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create data for patients from other hospitals."
            )

        return models.BloodTestImageData.objects.create(
            blood_test_id=blood_test_id, **validated_data
        )


class ResultImageDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResultImageData
        fields = [
            "id",
            "image",
            "result",
        ]

    def create(self, validated_data):
        result_id = self.context["result_id"]
        user_hospital_id = self.context["request"].user.hospital.id
        result_hospital = validated_data["result"].bloodtest.patient.hospital.id

        if str(result_hospital) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create data for patients from other hospitals."
            )

        return models.ResultImageData.objects.create(
            result_id=result_id, **validated_data
        )


class ResultSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    result_images = ResultImageDataSerializer(many=True, read_only=True)

    class Meta:
        model = models.Result
        fields = ["id", "created_at", "description", "result_images", "bloodtest"]

    def create(self, validated_data):
        blood_test_id = self.context["blood_test_id"]
        user_hospital_id = self.context["request"].user.hospital.id
        blood_test_hospital = validated_data["bloodtest"].patient.hospital.id

        if str(blood_test_hospital) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create data for patients from other hospitals."
            )

        return models.Result.objects.create(
            bloodtest_id=blood_test_id, **validated_data
        )


class BloodTestSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    images = BloodTestImageDataSerializer(many=True, read_only=True)

    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = models.BloodTest
        fields = [
            "id",
            "title",
            "description",
            "images",
            "results",
            "patient",
        ]

    def create(self, validated_data):
        patient_id = self.context["patient_id"]
        user_hospital_id = self.context["request"].user.hospital.id
        patient_hospital_id = validated_data["patient"].hospital.id

        if str(patient_hospital_id) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create data for patients from other hospitals."
            )

        return models.BloodTest.objects.create(patient_id=patient_id, **validated_data)


class PatientSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    blood_tests = BloodTestSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

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

    def create(self, validated_data):
        hospital_id = self.context["hospital_id"]
        user_hospital_id = self.context["request"].user.hospital.id

        if str(hospital_id) != str(user_hospital_id):
            raise serializers.ValidationError(
                "You cannot create patient data for other hospitals."
            )

        return models.Patient.objects.create(hospital_id=hospital_id, **validated_data)
