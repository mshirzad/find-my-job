from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestPublicUserAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        
        params = {
            'email': 'test@findmyjob.com',
            'password': 'test@123',
            'name': 'Test User'
        }

        resp = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(params['password']))
        self.assertNotIn('password', resp.data)

    def test_duplicate_user(self):

        params = {
            'email': 'test@findmyjob.com',
            'password': 'test@123',
            'name': 'Test User'
        }

        create_user(**params)

        resp = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):

        params = {
            'email': 'test@findmyjob.com',
            'password': 'sp',
            'name': 'Test User'
        }

        resp = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        dp_user = get_user_model().objects.filter(
            email = params['email']
        ).exists()
        self.assertFalse(dp_user)
        
    def test_token_created_for_user(self):

        params = {'email': 'test@findmyjob.com', 'password': 'test@123'}
        create_user(**params)

        resp = self.client.post(TOKEN_URL, params)
        self.assertIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_token_not_created_no_user(self):

        params = {'email': 'test@findmyjob.com', 'password': 'test@123'}
        
        resp = self.client.post(TOKEN_URL, params)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_invalid_cridentials(self):

        create_user(email='test@findmyjob.com', password='test@123')
        params = {'email': 'test@findmyjob.com', 'password': 'wrongpassword'}

        resp = self.client.post(TOKEN_URL, params)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_missing_fields(self):

        params = {'email': 'notvalidemail', 'password': ''}

        resp = self.client.post(TOKEN_URL, params)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_unauthorized_user(self):

        resp = self.client.get(ME_URL)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateAPI(TestCase):

    def setUp(self):
        
        self.user = create_user(
            email='test@findmyjob.com',
            password='test@1234',
            name='Test User'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile(self):

        resp = self.client.get(ME_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_method_not_allowed(self):

        resp = self.client.post(ME_URL, {})

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile(self):

        params = {
            'name': 'new name',
            'password': 'newpassword123@'
        }

        resp = self.client.patch(ME_URL, params)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, params['name'])
        self.assertTrue(self.user.check_password(params['password']))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        
