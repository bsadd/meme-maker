from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from accounts.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mainuser', password='password', email="testuser@localhost")
        self.user_data = {'username': 'mainuser', 'first_name': '', 'last_name': ''}
        Token.objects.create(user=self.user)

    def test_user_register(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('rest-auth-registration:rest_register')
        payload = {'username': 'testuser',
                   'password1': 'Xy12Pq34',
                   'password2': 'Xy12Pq34'}

        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_register = str(response.data['key'])

        """
        Verify registered user can login
        """
        url = reverse('rest-auth:rest_login')
        payload = {'username': 'testuser', 'password': 'Xy12Pq34', }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], token_register)

    def test_token_login(self):
        """
        Ensure we login to an existing account object via token authentication.
        """
        url = reverse('api:user-current')
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(self.user_data[k] == response.data[k] for k in self.user_data.keys() & response.data.keys()))

    def test_login(self):
        """
        Ensure we login to an existing account object via token authentication.
        """
        self.assertEqual(self.client.login(username='mainuser', password='password'), True)
        self.assertEqual(self.client.login(username='notuser', password='password'), False)

    def test_logout(self):
        self.assertEqual(self.client.login(username='mainuser', password='password'), True)
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('api:user-current')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(self.user_data[k] == response.data[k] for k in self.user_data.keys() & response.data.keys()))
        self.client.logout()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
