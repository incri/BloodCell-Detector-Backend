from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()


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
