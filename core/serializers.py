from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from lab.serializers import HospitalSerializer


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
            "is_hospital_admin",
        ]

    def create(self, validated_data):
        if "hospital" not in validated_data:
            validated_data["hospital"] = self.context["request"].user.hospital
        return super().create(validated_data)


class UserSerializer(BaseUserSerializer):

    hospital = HospitalSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "hospital",
            "is_hospital_admin",
        ]


class CustomTokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        refresh = RefreshToken.for_user(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "username": user.username,
                "is_hospital_admin": user.is_hospital_admin,
                "is_superuser": user.is_superuser,
                "full_name": user.first_name + " " + user.last_name,
            },
        }

        return data
