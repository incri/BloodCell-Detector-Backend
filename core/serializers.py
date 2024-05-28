from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from . import models



class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "hospital",
            "is_hospital_admin"
        ]

    def create(self, validated_data):
        validated_data['is_hospital_admin'] = True
        if 'hospital' not in validated_data:
            validated_data['hospital'] = self.context['request'].user.hospital
        return super().create(validated_data)


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]



class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = [
            "name",
            "address",
            "phone",
            "email",
            
        ]
