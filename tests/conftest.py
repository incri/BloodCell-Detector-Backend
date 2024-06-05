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
    def do_authenticate(is_staff=True, is_superuser=False, hospital_id=None):
        user = User.objects.create_user(username="testuser", password="testpass")
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        if hasattr(user, "hospital_id"):
            user.hospital_id = hospital_id
        user.save()
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


@pytest.fixture
def create_hospital_data():
    def do_create_hospital(hospital_id):
        return Hospital.objects.create(id=hospital_id, name="Test Hospital")

    return do_create_hospital


@pytest.fixture
def hospital_authenticate(api_client, create_hospital_data):
    def do_authenticate(is_staff=True, is_superuser=False, hospital_id=None):
        hospital = create_hospital_data(hospital_id)
        user = User.objects.create_user(
            username="testuser", password="testpass", hospital=hospital
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


# @pytest.fixture
# def create_blood_test(api_client):
#     def do_create_blood_test(blood_test):
#         return api_client.post('/lab/blood-tests/', blood_test)
#     return do_create_blood_test

# @pytest.fixture
# def create_blood_test_result(api_client):
#     def do_create_blood_test_result(blood_test_id, blood_test_result):
#         return api_client.post(f'/lab/blood-tests/{blood_test_id}/results/', blood_test_result)
#     return do_create_blood_test_result
