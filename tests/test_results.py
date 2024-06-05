# from rest_framework import status
# from rest_framework.test import force_authenticate

# import pytest
# from model_bakery import baker
# from lab.models import Patient
# from lab.models import Hospital


# @pytest.mark.django_db
# class TestCreateResults:

#     def test_if_user_is_anonymous_returns_401(self, create_blood_test_result):

#         # Arrange

#         # Act
#         blood_test = baker.make('lab.BloodTest')
#         blood_test_id = blood_test.id

#         # Act
#         response = create_blood_test_result(blood_test_id, {
#             'descriptions': 'Some result data',
#         })

#         # Assert
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED


#     def test_if_data_is_valid_returns_201(self, create_blood_test_result, hospital_authenticate):
#         # Arrange
#         hospital_authenticate(is_hospital_admin=True)
#         blood_test = baker.make('lab.BloodTest')
#         blood_test_id = blood_test.id


#         # Act
#         response = create_blood_test_result(blood_test_id, {
#             'description': 'Some result data',
#         })

#         # Assert
#         assert response.status_code == status.HTTP_201_CREATED


#     def test_if_data_is_invalid_returns_400(self, create_blood_test_result, hospital_authenticate):
#         # Arrange
#         hospital_authenticate(is_hospital_admin=True)
#         blood_test = baker.make('lab.BloodTest')
#         blood_test_id = blood_test.id

#         #Act

#         response = create_blood_test_result(blood_test_id, {
#             'description': '',
#         })

#         # Assert
#         assert response.status_code == status.HTTP_400_BAD_REQUEST


# @pytest.mark.django_db
# class TestRetrieveResults:


#     def test_if_results_exists_and_user_is_not_authenticated_returns_402(self, api_client, create_blood_test_result, create_patient, create_blood_test, hospital_authenticate):

#         hospital_authenticate(is_hospital_admin=True)


#         # Arrange

#         patient_response = create_patient({
#             'first_name': 'a',
#             'last_name': 'a',
#             'email': 'a@gmail.com',
#             'phone': 'a',
#             'birth_date': '2002-04-02',
#         })
#         patient_id = patient_response.json().get('id')

#         # Act
#         blood_test = create_blood_test({
#             'title': 'Blood Test Title',
#             'description': 'Detailed description of the blood test',
#             'detection_status': 'P',
#             'patient':patient_id
#         })

#         blood_test_id = blood_test.json().get('id')


#         results = create_blood_test_result(blood_test_id, {
#             'description': 'Some result data',
#         })

#         api_client.force_authenticate(user=None)


#         # Act

#         response = api_client.get(f'/lab/blood-tests/{blood_test_id}/results/{results.json().get('id')}/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED


#     def test_if_results_exists_and_user_is_authenticated_returns_200(self, api_client, hospital_authenticate, create_blood_test_result, create_patient, create_blood_test):


#         # Arrange
#         hospital_authenticate(is_hospital_admin=True)

#         patient_response = create_patient({
#             'first_name': 'a',
#             'last_name': 'a',
#             'email': 'a@gmail.com',
#             'phone': 'a',
#             'birth_date': '2002-04-02',
#         })
#         patient_id = patient_response.json().get('id')

#         # Act
#         blood_test = create_blood_test({
#             'title': 'Blood Test Title',
#             'description': 'Detailed description of the blood test',
#             'detection_status': 'P',
#             'patient':patient_id
#         })

#         blood_test_id = blood_test.json().get('id')


#         results = create_blood_test_result(blood_test_id, {
#             'description': 'Some result data',
#         })


#         # Act

#         response = api_client.get(f'/lab/blood-tests/{blood_test_id}/results/{results.json().get('id')}/')

#         assert response.status_code == status.HTTP_200_OK


#     def test_if_results_does_not_exists_returns_404(self, api_client, create_patient, hospital_authenticate, create_blood_test, create_blood_test_result):

#         hospital_authenticate(is_hospital_admin=True)

#         patient_response = create_patient({
#             'first_name': 'a',
#             'last_name': 'a',
#             'email': 'a@gmail.com',
#             'phone': 'a',
#             'birth_date': '2002-04-02',
#         })
#         patient_id = patient_response.json().get('id')

#         # Act
#         blood_test = create_blood_test({
#             'title': 'Blood Test Title',
#             'description': 'Detailed description of the blood test',
#             'detection_status': 'P',
#             'patient':patient_id
#         })

#         blood_test_id = blood_test.json().get('id')


#         results = create_blood_test_result(blood_test_id, {
#             'description': 'Some result data',
#         })


#         response = api_client.get(f'/lab/blood-tests/{blood_test_id}/results/1/')

#         assert response.status_code == status.HTTP_404_NOT_FOUND
