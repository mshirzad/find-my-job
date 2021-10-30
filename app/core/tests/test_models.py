from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_sample_user(email='test@findmyjob.com', password='test@1234'):
    return get_user_model().objects.create_user(email,password)


class TestModel(TestCase):

    def test_user_creation(self):

        email = 'test@findmyjob.com'
        password = 'test123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):

        email = 'test@FINDMYJOB.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_user_email_validation(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_superuser_creation(self):
        
        email = 'test@FINDMYJOB.COM'
        user = get_user_model().objects.create_superuser(email, 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_string_rep_of_profile(self):
        
        addr = models.Address.objects.create(
            country='AFG',
            city='KBL',
            distrect=4,
            street='4th',
            address_line='Behind Jahan Uni'
        )

        profile = models.Profile.objects.create(
            name='Ahmad',
            last_name='Shirzad',
            phone=774488929,
            profession='Eng',
            base_addr = addr,
            user = create_sample_user()
        )

        self.assertEqual(str(profile), profile.name)