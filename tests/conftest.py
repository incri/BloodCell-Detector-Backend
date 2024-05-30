from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest
from model_bakery import baker
from hospital.models import Hospital


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


@pytest.fixture
def hospital_authenticate(api_client):
    def do_authenticate(is_hospital_admin=False):
        hospital = baker.make(Hospital)
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com',
            is_hospital_admin=is_hospital_admin,
            hospital=hospital
        )
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate


