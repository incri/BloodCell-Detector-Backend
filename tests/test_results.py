from rest_framework import status

# from rest_framework.test import force_authenticate

import pytest

from model_bakery import baker

# from lab.models import Patient
# from lab.models import Hospital


@pytest.fixture
def create_result(api_client):
    def do_create_result(result_data, hospital_id, patient_id, blood_test_id):
        url = f"/hospitals/{hospital_id}/patients/{patient_id}/blood-tests/{blood_test_id}/results/"
        return api_client.post(url, result_data)

    return do_create_result


@pytest.mark.django_db
class TestCreateResults:

    def test_if_user_is_anonymous_returns_401(
        self, create_result, authenticate, api_client
    ):

        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test = baker.make("BloodTest", patient=patient)

        result_data = {
            "description": "Detailed description of the blood test",
            "bloodtest": blood_test.id,
        }

        api_client.force_authenticate(user=None)

        # Act
        response = create_result(
            result_data,
            hospital.id,
            patient.id,
            blood_test.id,
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, create_result, authenticate):
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test = baker.make("BloodTest", patient=patient)

        result_data = {
            "description": "Detailed description of the blood test",
            "bloodtest": blood_test.id,
        }

        # Act
        response = create_result(
            result_data,
            hospital.id,
            patient.id,
            blood_test.id,
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, create_result, authenticate):

        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test = baker.make("BloodTest", patient=patient)

        result_data = {
            "description": "",
            "bloodtest": blood_test.id,
        }

        # Act
        response = create_result(
            result_data,
            hospital.id,
            patient.id,
            blood_test.id,
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveResults:

    def test_if_results_exists_and_user_is_not_authenticated_returns_401(
        self,
        api_client,
        authenticate,
    ):

        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital

        blood_test = baker.make(
            "BloodTest", patient=patient
        )  # Create a patient associated with the hospital

        result = baker.make("Result", bloodtest=blood_test)

        # Act

        api_client.force_authenticate(user=None)

        response = api_client.get(
            f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/{blood_test.id}/results/{result.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_results_exists_and_user_is_authenticated_returns_200(
        self,
        api_client,
        authenticate,
    ):

        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital

        blood_test = baker.make(
            "BloodTest", patient=patient
        )  # Create a patient associated with the hospital

        result = baker.make("Result", bloodtest=blood_test)

        # Act

        response = api_client.get(
            f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/{blood_test.id}/results/{result.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_results_does_not_exists_returns_404(
        self,
        api_client,
        authenticate,
    ):

        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital

        blood_test = baker.make(
            "BloodTest", patient=patient
        )  # Create a patient associated with the hospital

        result = baker.make("Result", bloodtest=blood_test)

        # Act

        response = api_client.get(
            f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/{blood_test.id}/results/1/"
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
