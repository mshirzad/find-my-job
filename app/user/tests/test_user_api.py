from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

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