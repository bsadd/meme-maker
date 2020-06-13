from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from accounts.models import User


class PostTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin', email='admin@localhost')
        self.moderator = User.objects.create_user(username='moderator', password='moderator', email='admin@localhost')
        self.key_admin = Token.objects.create(user=self.admin).key
        self.key_moderator = Token.objects.create(user=self.moderator).key

        url = reverse('rest-auth-registration:rest_register')
        self.keys = []
        users = [
            User(username='user1', password='Xy12Pq341'),
            User(username='user2', password='Xy12Pq342'),
            User(username='user3', password='Xy12Pq343')
        ]
        for user in users:
            response = self.client.post(url, data={'username': user.username, 'password1': user.password,
                                                   'password2': user.password}, format='json')
            self.keys.append(str(response.data['key']))

    def test_create(self):
        """
        Ensure we can create a new post object.
        """
        pass

    def test_update(self):
        """
        Ensure we can update an existing post object only via author
        """
        pass

    def test_react(self):
        """
        Ensure only authenticated user can react on an existing approved post object only
        """
        pass

    def test_reactCount(self):
        """
        Ensure react count only increases/decreases with authenticated user's react
        """
        pass

    def test_approve(self):
        """
        Ensure only moderators can approve/reject a post object
        """
        pass
