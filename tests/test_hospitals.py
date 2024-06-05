from rest_framework import status
import pytest

from model_bakery import baker
from lab.models import Hospital


@pytest.fixture
def create_hospital(api_client):
    def do_create_hospital(hospital):
        return api_client.post("/hospitals/", hospital)

    return do_create_hospital


@pytest.mark.django_db
class TestCreateHospital:

    def test_if_user_is_anonymous_returns_401(self, create_hospital):

        # Arrange

        # Act
        response = create_hospital(
            {
                "name": "a",
                "address": "a",
                "phone": "a",
                "email": "a@gmail.com",
            }
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_hospital, authenticate):

        # Arrange
        authenticate()

        # Act
        response = create_hospital(
            {
                "name": "a",
                "address": "a",
                "phone": "a",
                "email": "a@gmail.com",
            }
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_hospital, authenticate):
        # Arrange
        authenticate(is_superuser=True)

        # Act
        response = create_hospital(
            {
                "name": "",
                "address": "a",
                "phone": "a",
                "email": "agmail.com",
            }
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, api_client, create_hospital, authenticate
    ):

        # Arrange
        authenticate(is_superuser=True)

        # Act
        response = create_hospital(
            {"name": "a", "address": "a", "phone": "a", "email": "a@gmail.com"}
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveHospital:

    def test_if_hospital_exists_and_user_is_not_admin_returns_403(
        self, api_client, authenticate
    ):

        authenticate()

        hospital = baker.make(Hospital)

        response = api_client.get(f"/hospitals/{hospital.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_hospital_exists_and_user_is_anonymous_returns_401(self, api_client):

        hospital = baker.make(Hospital)

        response = api_client.get(f"/hospitals/{hospital.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_hospital_exists_returns_200(self, api_client, authenticate):

        authenticate(is_superuser=True)

        hospital = baker.make(Hospital)

        response = api_client.get(f"/hospitals/{hospital.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_if_hospital_does_not_exists_returns_404(self, api_client, authenticate):

        authenticate(is_superuser=True)

        response = api_client.get("/hospitals/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
