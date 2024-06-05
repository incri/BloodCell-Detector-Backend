from rest_framework import status
from rest_framework.test import force_authenticate

import pytest
from django.urls import reverse

from model_bakery import baker
from lab.models import Patient
from lab.models import Hospital


@pytest.fixture
def create_patient(api_client):
    def do_create_patient(patient_data, hospital_id):
        url = f"/hospitals/{hospital_id}/patients/"
        return api_client.post(url, patient_data)

    return do_create_patient


@pytest.mark.django_db
class TestCreatePatient:

    def test_if_user_is_anonymous_returns_401(self, create_patient):

        # Arrange

        # Act
        patient_data = {
            "first_name": "a",
            "last_name": "a",
            "email": "a@gmail.com",
            "phone": "a",
            "birth_date": "2002-04-02",
        }

        # Act
        response = create_patient(patient_data, 1)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(
        self, create_patient, hospital_authenticate
    ):

        # Arrange
        hospital_authenticate(hospital_id=1)
        patient_data = {
            "first_name": "",
            "last_name": "a",
            "email": "a@gmail.com",
            "phone": "a",
            "birth_date": "2002-04-02",
        }

        # Act
        response = create_patient(patient_data, 1)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_patient, hospital_authenticate):
        # Arrange
        hospital_authenticate(hospital_id=1)
        patient_data = {
            "first_name": "a",
            "last_name": "a",
            "email": "a@gmail.com",
            "phone": "a",
            "birth_date": "2002-04-02",
        }

        # Act
        response = create_patient(patient_data, 1)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED


# @pytest.mark.django_db
# class TestRetrievePatient:


#     def test_if_patients_exists_and_user_is_not_authenticated_returns_401(self, api_client, create_patient, hospital_authenticate):

#         hospital_authenticate(is_hospital_admin=False)

#         patient = create_patient({
#             'first_name': 'a',
#             'last_name': 'a',
#             'email': 'a@gmail.com',
#             'phone': 'a',
#             'birth_date': '2002-04-02',
#         })

#         api_client.force_authenticate(user=None)

#         response = api_client.get(f'/lab/patients/{patient.json().get('id')}/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED


#     def test_if_patients_exists_returns_200(self, api_client, create_patient, hospital_authenticate):
#     # Arrange
#         hospital_authenticate(is_hospital_admin=False)
#         # Act
#         patient = create_patient({
#             'first_name': 'a',
#             'last_name': 'a',
#             'email': 'a@gmail.com',
#             'phone': 'a',
#             'birth_date': '2002-04-02',
#         })

#         response = api_client.get(f'/lab/patients/{patient.json().get('id')}/')

#         # Assert
#         assert response.status_code == status.HTTP_200_OK


#     def test_if_patients_does_not_exists_returns_404(self, api_client, hospital_authenticate):

#         hospital_authenticate(is_hospital_admin=True)

#         response = api_client.get(f'/lab/patients/1/')

#         assert response.status_code == status.HTTP_404_NOT_FOUND
