from rest_framework import status
import pytest
from model_bakery import baker
from lab.models import Patient
from hospital.models import Hospital

@pytest.fixture
def create_patient(api_client):
    def do_create_patient(patient):
        return api_client.post('/lab/patients/', patient)
    return do_create_patient



@pytest.mark.django_db
class TestCreatePatient:

    def test_if_user_is_anonymous_returns_401(self, create_patient):

        # Arrange

        # Act
        response = create_patient({
            'first_name' : 'a',
            'last_name' : 'a',
            'email' : 'a@gmail.com',
            'phone' : 'a',
            'birth_date' : '2002-04-02',
        })

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_data_is_invalid_returns_400(self, create_patient, hospital_authenticate):

        # Arrange
        hospital_authenticate(is_hospital_admin=True)


        # Act
        response = create_patient({
            'first_name' : 'a',
            'last_name' : 'a',
            'email' : 'agmail.com',
            'phone' : 'a',
            'birth_date' : '2002-04-02',
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_patient, hospital_authenticate):
    # Arrange
        hospital_authenticate(is_hospital_admin=False)
        # Act
        response = create_patient({
            'first_name': 'a',
            'last_name': 'a',
            'email': 'a@gmail.com',
            'phone': 'a',
            'birth_date': '2002-04-02',
        })

        # Assert
        assert response.status_code == status.HTTP_201_CREATED


    



@pytest.mark.django_db
class TestRetrievePatient:


    def test_if_collection_exists_and_user_is_not_authenticated_returns_401(self, api_client, create_patient):

        patient = create_patient({
            'first_name': 'a',
            'last_name': 'a',
            'email': 'a@gmail.com',
            'phone': 'a',
            'birth_date': '2002-04-02',
        })

        response = api_client.get(f'/lab/patients/{patient.json().get('id')}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED



    def test_if_collection_exists_returns_200(self, api_client, create_patient, hospital_authenticate):
    # Arrange
        hospital_authenticate(is_hospital_admin=False)
        # Act
        patient = create_patient({
            'first_name': 'a',
            'last_name': 'a',
            'email': 'a@gmail.com',
            'phone': 'a',
            'birth_date': '2002-04-02',
        })

        response = api_client.get(f'/lab/patients/{patient.json().get('id')}/')

        # Assert
        assert response.status_code == status.HTTP_200_OK


    def test_if_collection_does_not_exists_returns_404(self, api_client, hospital_authenticate):

        hospital_authenticate(is_hospital_admin=True)

        response = api_client.get(f'/lab/patients/1/')

        assert response.status_code == status.HTTP_404_NOT_FOUND