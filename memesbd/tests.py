from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from memesbd.consts_db import ApprovalStatus
from memesbd.models import Post

from PIL import Image
import tempfile
import io
import base64


class PostTests(APITestCase):
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()
        self.admin = User.objects.create_superuser(username='admin', password='admin', email='admin@localhost')
        self.moderator = User.objects.create_user(username='moderator', password='moderator', email='admin@localhost')
        self.moderator.is_moderator = True
        self.moderator.save()
        self.key_admin = Token.objects.create(user=self.admin).key
        self.key_moderator = Token.objects.create(user=self.moderator).key

        url = reverse('rest-auth-registration:rest_register')
        self.keys = []
        users = [
            User(username='user0', password='Xy12Pq341'),
            User(username='user1', password='Xy12Pq342'),
            User(username='user2', password='Xy12Pq343')
        ]
        for user in users:
            response = self.client.post(url, data={'username': user.username, 'password1': user.password,
                                                   'password2': user.password}, format='json')
            self.keys.append(str(response.data['key']))

        self.tmp_file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")

        self.post_unapproved = Post.objects.create(caption='unapproved_post',
                                                   author=User.objects.get(username='user2'))

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(1024, 1024), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_new_create(self):
        """
        Ensure we can create a new post object.
        TODO: file upload support
        """
        ## user0
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-list')
        payload = {'caption': 'new_post',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': [{'name': 'me'}, {'name': 'me2'}],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['username'], 'user0')
        self.assertEqual(response.data['approval_status'], 'PENDING')
        # self.assertEqual(str(response.data['image']).split('/')[-1], self.generate_photo_file().name)
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

        ## user1 on repeated keyword
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'new_post',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': [{'name': 'me'}, {'name': 'me3'}],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['username'], 'user1')
        self.assertEqual(response.data['approval_status'], 'PENDING')
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

    def test_update(self):
        """
        Ensure we can update an existing post object only via author
        """
        pass

    def test_react(self):
        """
        Ensure only authenticated user can react on an existing approved post object only
        """
        post_approved = Post.objects.create(caption='approved_post', approval_status=ApprovalStatus.APPROVED,
                                            author=User.objects.get(username='user2'))
        ## Anonymous user
        url = reverse('api:post-react-list', args=[post_approved.id])
        payload = {'react': 'love'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        ## user0 invalid react
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved.id])
        payload = {'react': 'liked'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 react on unapproved post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[self.post_unapproved.id])
        payload = {'react': 'like'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 react on invalid post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[100])
        payload = {'react': 'like'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 - react LOVE
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved.id])
        payload = {'react': 'love'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['post'], post_approved.id)
        self.assertEqual(response.data['react'], 'LOVE')

        ## user0 - check react LOVE
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-user', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['react'], 'LOVE')

        ## user0 change react to HAHA
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved.id])
        payload = {'react': 'haha'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['post'], post_approved.id)
        self.assertEqual(response.data['react'], 'HAHA')

        ## user0 - check react HAHA
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-user', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['react'], 'HAHA')

    def test_reactCount(self):
        """
        Ensure react count only increases/decreases with authenticated user's react
        """
        post_approved = Post.objects.create(caption='approved_post', approval_status=ApprovalStatus.APPROVED,
                                            author=User.objects.get(username='user2'))
        post_approved_2 = Post.objects.create(caption='approved_post_2', approval_status=ApprovalStatus.APPROVED,
                                              author=User.objects.get(username='user2'))
        ## initially no react
        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['react_counts'], {})

        ## user0 - react LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved.id])
        response = self.client.post(url, data={'react': 'love'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ## user0 - react LIKE - post2
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved_2.id])
        response = self.client.post(url, data={'react': 'like'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['react_counts'], {'LOVE': 1})

        ## user1 - react LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-react-list', args=[post_approved.id])
        response = self.client.post(url, data={'react': 'love'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['react_counts'], {'LOVE': 2})

        ## user2 - react HAHA - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[2])
        url = reverse('api:post-react-list', args=[post_approved.id])
        response = self.client.post(url, data={'react': 'haha'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['react_counts'], {'LOVE': 2, 'HAHA': 1})

        ## user0 - unreact LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-react-list', args=[post_approved.id])
        response = self.client.post(url, data={'react': 'none'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['react_counts'], {'LOVE': 1, 'HAHA': 1})

    def test_approval(self):
        """
        Ensure only moderators can approve/reject a post object
        """
        # initially pending & hence cannot get the post
        url = reverse('api:post-detail', args=[self.post_unapproved.id])
        self.assertEqual(self.post_unapproved.approval_status, ApprovalStatus.PENDING)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # normal user cannot approve the post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[2])
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.post(url, data={'approval_status': 'APPROVED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # moderator approves the post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.key_moderator)
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.put(url, data={'approval_status': 'APPROVED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['approval_status'], 'APPROVED')

        # moderator tries to approve the already approved post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.key_moderator)
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.put(url, data={'approval_status': 'APPROVED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # post is accessible after being approved
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('api:post-detail', args=[self.post_unapproved.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['approval_status'], 'APPROVED')

        # admin rejects the post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.key_admin)
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.put(url, data={'approval_status': 'REJECTED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['approval_status'], 'REJECTED')

        # post is not accessible after being rejected
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[2])
        url = reverse('api:post-detail', args=[self.post_unapproved.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # moderator tries to reject the already rejected post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.key_moderator)
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.put(url, data={'approval_status': 'REJECTED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
