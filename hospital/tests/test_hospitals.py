from django.contrib.auth.models import User
from rest_framework import status
import pytest


@pytest.fixture
def create_hospital(api_client):
    def do_create_hospital(hospital):
        return api_client.post('/hospital/create/', hospital)
    return do_create_hospital



@pytest.mark.django_db
class TestCreateHospital:
    def test_if_user_is_anonymous_returns_401(self, create_hospital):

        # Arrange

        # Act
        response = create_hospital({
            'name': 'a',
            'address': 'a',
            'phone': 'a',
            'email': 'a@gmail.com'
        })

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    @pytest.mark.django_db
    def test_if_user_is_not_admin_returns_403(self, api_client, create_hospital, authenticate):

        # Arrange
        authenticate(is_staff=False)

        # Act
        response = create_hospital({
            'name': 'a',
            'address': 'a',
            'phone': 'a',
            'email': 'a@gmail.com'
        })

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_if_data_is_invalid_returns_400(self, api_client, create_hospital, authenticate):

        # Arrange
        authenticate(is_staff=True)

        # Act
        response = create_hospital({
            'name': '',
            'address': 'a',
            'phone': 'a',
            'email': 'a@gmail.com'
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    @pytest.mark.django_db
    def test_if_data_is_valid_returns_200(self, api_client, create_hospital, authenticate):

        # Arrange
        authenticate(is_staff=True)

        # Act
        response = create_hospital({
            'name': 'a',
            'address': 'a',
            'phone': 'a',
            'email': 'a@gmail.com'
        })

        # Assert
        assert response.status_code == status.HTTP_201_CREATED


