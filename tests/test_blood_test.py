from rest_framework import status

# from rest_framework.test import force_authenticate
import pytest

from model_bakery import baker

# from lab.models import Patient
# from lab.models import Hospital


@pytest.fixture
def create_blood_test(api_client):
    def do_create_blood_test(blood_test_data, hospital_id, patient_id):
        url = f"/hospitals/{hospital_id}/patients/{patient_id}/blood-tests/"
        return api_client.post(url, blood_test_data)

    return do_create_blood_test


@pytest.mark.django_db
class TestCreateBloodTest:

    def test_if_user_is_anonymous_returns_401(self, create_blood_test):

        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test_data = {
            "title": "Blood Test Title",
            "description": "Detailed description of the blood test",
            "detection_status": "P",
            "patient": patient.id,
        }

        # Act
        response = create_blood_test(blood_test_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, create_blood_test, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test_data = {
            "title": "Blood Test Title",
            "description": "Detailed description of the blood test",
            "detection_status": "P",
            "patient": patient.id,
        }

        # Act
        response = create_blood_test(blood_test_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, create_blood_test, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        # Act
        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated w

        blood_test_data = {
            "title": "",
            "description": "",
            "detection_status": "P",
            "patient": patient.id,
        }

        # Act
        response = create_blood_test(blood_test_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveBloodTest:

    # def test_if_blood_test_exists_and_user_is_not_authenticated_returns_401(
    #     self, api_client, authenticate
    # ):

    #     # Arrange
    #     hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
    #     authenticate(hospital_id=hospital.id)

    #     # Act
    #     patient = baker.make(
    #         "Patient", hospital=hospital
    #     )  # Create a patient associated w

    #     blood_test = baker.make(
    #         "BloodTest", patient=patient
    #     )  # Create a patient associated w

    #     api_client.force_authenticate(user=None)

    #     response = api_client.get(
    #         f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/{blood_test.id}/"
    #     )

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_patients_exists_returns_200(
        self,
        api_client,
        authenticate,
        create_blood_test,
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

        # Act

        response = api_client.get(
            f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/{blood_test.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_blood_test_does_not_exists_returns_404(self, api_client, authenticate):

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

        # Act

        response = api_client.get(
            f"/hospitals/{hospital.id}/patients/{patient.id}/blood-tests/1/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
