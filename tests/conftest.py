from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest
from model_bakery import baker
from lab.models import Hospital


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


@pytest.fixture
def create_patient(api_client):
    def do_create_patient(patient):
        return api_client.post('/lab/patients/', patient)
    return do_create_patient

@pytest.fixture
def create_blood_test(api_client):
    def do_create_blood_test(blood_test):
        return api_client.post('/lab/blood-tests/', blood_test)
    return do_create_blood_test

@pytest.fixture
def create_blood_test_result(api_client):
    def do_create_blood_test_result(blood_test_id, blood_test_result):
        return api_client.post(f'/lab/blood-tests/{blood_test_id}/results/', blood_test_result)
    return do_create_blood_test_result
