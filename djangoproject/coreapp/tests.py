from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from coreapp.consts_db import ApprovalStatus
from coreapp.models import Post

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
                                                   user=User.objects.get(username='user2'))

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(1024, 1024), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_create_template(self):
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
                   'keywords': ['me', 'me2'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user0')
        self.assertEqual(response.data['approval_status'], 'Pending')
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

        ## user1 on repeated keyword
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'new_post',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': ['me', 'me3'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user1')
        self.assertEqual(response.data['approval_status'], 'Pending')
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

        ## user1 w/o keywords
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'new_post',
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user1')
        self.assertEqual(response.data['approval_status'], 'Pending')
        payload['keywords'] = []
        payload['template'] = None
        payload['is_adult'] = payload['is_violent'] = False
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

    def test_create_from_template(self):
        """
        Ensure we can create a post object from a template.
        """
        template_post = Post.objects.create(caption="template_approved_post", user=User.objects.get(username='user0'),
                                            moderator=self.moderator, approval_status=ApprovalStatus.APPROVED)
        template_post_url = self.client.get(reverse('api:post-detail', args=[template_post.id])).data['url']

        ## user0
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-list')
        payload = {'caption': 'from_template_post',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': ['me', 'me2'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': template_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user0')
        self.assertEqual(response.data['approval_status'], 'Pending')
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

        ## user1 on repeated keyword
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'from_template_post2',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': ['me', 'me3'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': template_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user1')
        self.assertEqual(response.data['approval_status'], 'Pending')
        self.assertTrue(
            all(payload[k] == response.data[k] for k in payload.keys() & response.data.keys() if k != 'image'))

        ## create from non-existing template post
        template_post_url = "http://testserver" + reverse('api:post-detail', args=[1000])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'from_template_post2',
                   'keywords': ['me', 'me1'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': template_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## create from unapproved template post
        template_post_url = "http://testserver" + reverse('api:post-detail', args=[self.post_unapproved.id])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'from_template_post2',
                   'keywords': ['me', 'me2'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': template_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_from_nested_template(self):
        """
        Ensure base template reference is maintained when we create a post object from another post which is itself created from a template.
        """
        base_template = Post.objects.create(caption="template_approved_post",
                                            user=User.objects.get(username='user0'),
                                            moderator=self.moderator, approval_status=ApprovalStatus.APPROVED,
                                            template_id=None)
        generated_post = Post.objects.create(caption="template_approved_post",
                                             user=User.objects.get(username='user0'),
                                             moderator=self.moderator, approval_status=ApprovalStatus.APPROVED,
                                             template=base_template)
        template_post_url = self.client.get(reverse('api:post-detail', args=[base_template.id])).data['url']
        generated_post_url = self.client.get(reverse('api:post-detail', args=[generated_post.id])).data['url']

        ## user0
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-list')
        payload = {'caption': 'from_generated_post',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': ['me', 'me2'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': generated_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['template'], template_post_url)

        ## user1 on repeated keyword
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-list')
        payload = {'caption': 'from_generated_post2',
                   'is_adult': True,
                   'is_violent': False,
                   'keywords': ['me', 'me3'],
                   'image': base64.b64encode(self.generate_photo_file().read()),
                   'template': generated_post_url,
                   }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'user1')
        self.assertEqual(response.data['template'], template_post_url)

    def test_update(self):
        """
        Ensure we can update an existing post object only via author
        """
        pass

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
        self.assertEqual(response.data['approval_status'], 'Approved')

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
        self.assertEqual(response.data['approval_status'], 'Approved')

        # admin rejects the post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.key_admin)
        url = reverse('api:moderation-post-detail', args=[self.post_unapproved.id])
        response = self.client.put(url, data={'approval_status': 'REJECTED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['approval_status'], 'Rejected')

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


class PostReactionTests(APITestCase):
    def setUp(self):
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

        self.post_unapproved = Post.objects.create(caption='unapproved_post',
                                                   user=User.objects.get(username='user2'))

    def test_reaction(self):
        """
        Ensure only authenticated user can reaction on an existing approved post object only
        """
        post_approved = Post.objects.create(caption='approved_post', approval_status=ApprovalStatus.APPROVED,
                                            user=User.objects.get(username='user2'))
        ## Anonymous user
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        payload = {'reaction': 'love'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        ## user0 invalid reaction
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        payload = {'reaction': 'liked'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 react on unapproved post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[self.post_unapproved.id])
        payload = {'reaction': 'like'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 react on invalid post
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[100])
        payload = {'reaction': 'like'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## user0 - react LOVE
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        payload = {'reaction': 'love'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['reaction'], 'Love')

        ## user0 - check reaction LOVE
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-user', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reaction'], 'Love')

        ## user0 change reaction to HAHA
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        payload = {'reaction': 'haha'}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['reaction'], 'Haha')

        ## user0 - check reaction HAHA
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-user', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reaction'], 'Haha')

    def test_reactionCount(self):
        """
        Ensure reaction count only increases/decreases with authenticated user's reaction
        """
        post_approved = Post.objects.create(caption='approved_post', approval_status=ApprovalStatus.APPROVED,
                                            user=User.objects.get(username='user2'))
        post_approved_2 = Post.objects.create(caption='approved_post_2', approval_status=ApprovalStatus.APPROVED,
                                              user=User.objects.get(username='user2'))
        ## initially no reaction
        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['reaction_counts'], {})

        ## user0 - react LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        response = self.client.post(url, data={'reaction': 'love'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ## user0 - react LIKE - post2
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved_2.id])
        response = self.client.post(url, data={'reaction': 'like'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['reaction_counts'], {'Love': 1})

        ## user1 - react LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[1])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        response = self.client.post(url, data={'reaction': 'love'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['reaction_counts'], {'Love': 2})

        ## user2 - react HAHA - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[2])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        response = self.client.post(url, data={'reaction': 'haha'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['reaction_counts'], {'Love': 2, 'Haha': 1})

        ## user0 - unreact LOVE - post1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.keys[0])
        url = reverse('api:post-reaction-list', args=[post_approved.id])
        response = self.client.post(url, data={'reaction': 'none'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:post-detail', args=[post_approved.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['reaction_counts'], {'Love': 1, 'Haha': 1})
