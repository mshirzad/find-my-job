import os, tempfile

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import test, status
from rest_framework.test import APIClient

from core.models import Profile, Address, Gig, Education

from freelancer.serializers import ProfileSerializer


# MY_PROFILE_URL = reverse('freelancer:myProfile-list')
# ALL_PROFILES_URL = reverse('freelancer:profile-list')

def upload_profile_photo_url(profile_id):
    return reverse('freelancer:myprofile-uploade-profile-photo', args=[profile_id])

def profile_details_url(profile_id):
    return reverse('freelancer:myprofile-details', args=[profile_id])

def create_sample_address(**params):
    defaults = {
        'address_line1': 'Apt 102, St 33 NW',
        'city': 'LA',
        'province': 'CA',
        'post_code': '33AW23',
        'country': 'USA'
    }

    defaults.update(params)

    return Address.objects.create(**defaults)

def create_sample_edu(**params):
    defaults = {
        'degree': 'Master',
        'university': 'MIT',
        'faculty': 'CS',
        'start_year': 2018,
        'graduation_year': 2020
    }

    defaults.update(params)

    return Education.objects.create(**defaults)

def create_sample_profile(user, **params):
    defaults = {
        'phone': '+93778898899',
        'profession': 'Eng',
        'boi': 'Test Boi',
        'address': create_sample_address(),
        'education': create_sample_edu()
    }

    defaults.update(params)

    return Profile.objects.create(user=user, **defaults)

def create_sample_gig(freelancer, **params):
    defaults = {
        'title': 'New Gig for Web App',
        'description': 'Some Lorem ipsom',
        'min_price': 40.00
    }

    defaults.update(params)

    return Gig.objects.create(freelancer=freelancer, **defaults)


# class TestPublicProfileAPI(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#     def test_auth_required(self):
#         resp = self.client.get(ALL_PROFILES_URL)

#         self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


# class TestPrivateProfileAPI(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#         self.user = get_user_model().objects.create_user(
#             email='test@findmyjob.com',
#             password='test@12345'
#         )

#         self.user.name = 'Test User'

#         self.client.force_authenticate(self.user)

#     def test_show_freelancer_profile_to_other_users(self):

#         user2 = get_user_model().objects.create_user(
#             'otheruser@findmyjob.com',
#             'test@1234555'
#         )
#         user2.name = 'Test USER'

#         user3 = get_user_model().objects.create_user(
#             'user3@findmyjob.com',
#             'test@1234555'
#         )
#         user3.name = 'Test USER3'

#         create_sample_profile(user=user2) 
#         create_sample_profile(user=user3) 

#         resp = self.client.get(ALL_PROFILES_URL)

#         profiles = Profile.objects.all().order_by('-rating')
#         serializer = ProfileSerializer(profiles, many=True)

#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data, serializer.data)

#     def test_show_profile_to_its_own_user(self):
#         user2 = get_user_model().objects.create_user(
#             'otheruser@findmyjob.com',
#             'test@1234555'
#         )

#         user2.name = 'Test USER2'

#         create_sample_profile(user=user2)
#         create_sample_profile(user=self.user)

#         resp = self.client.get(MY_PROFILE_URL)

#         profile = Profile.objects.filter(user=self.user)
#         serializer = ProfileSerializer(profile, many=True)

#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(resp.data), 1)
#         print(resp.data)
#         print("#########")
#         print(serializer.data)
#         self.assertEqual(resp.data, serializer.data)


# class TestUploadProfilePhotoAPI(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#         self.user = get_user_model().objects.create_user(
#             email='test@findmyjob.com',
#             password='test@12345'
#         )

#         self.user.name = 'Test User'

#         self.client.force_authenticate(self.user)
#         self.profile = create_sample_profile(user= self.user)

#     def tearDown(self):
#         self.profile.profile_photo.delete()

#     def test_upload_profile_photo(self):
#         url = upload_profile_photo_url(profile_id=self.profile.id)

#         with tempfile.NamedTemporaryFile(suffix='.jpg') as nft:
#             img = Image.new('RGB', (10,10))
#             img.save(nft, format='JPEG')
#             nft.seek(0)

#             resp = self.client.post(url, {'profile_photo': nft}, format='maltipart')

#         self.profile.refresh_form_db()
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertIn('profile_photo', resp.data)
#         self.assertTrue(os.path.exists(self.profile.profile_photo.path))

#     def test_upload_profile_photo_bad_image(self):
#         url = upload_profile_photo_url(profile_id=self.profile.id)
#         resp = self.client.post(url, {'profile_photo': 'noImage'}, format='maltipart')

#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
