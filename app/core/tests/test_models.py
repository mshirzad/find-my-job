from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_sample_user(email='test@findmyjob.com', password='test@1234', name='Test User'):
    user = get_user_model().objects.create_user(email, password)
    user.name = name

    return user

class TestModel(TestCase):

    def test_user_creation(self):

        email = 'test@findmyjob.com'
        password = 'test123'
        name = 'Test User'
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

    def test_string_rep_of_models(self):
        
        addr = models.Address.objects.create(
            address_line1='Apt No 1',
            city='KBL',
            province='KBL',
            post_code='1007T',
            country='AFG'
        )

        edu = models.Education.objects.create(
            degree='Phd',
            university='Kabul Uni',
            faculty='CS',
            start_year=2017,
            graduation_year=2021
        )

        
        profile = models.Profile.objects.create(
            phone='+93774484645',
            profession='CS',
            user=create_sample_user(),
            address=addr,
            education=edu,
        )

        gig = models.Gig.objects.create(
            title='Rest Full API',
            description='Develope a full functioning RestAPI',
            min_price=200.00,
            freelancer=profile
        )


        self.assertEqual(str(profile), profile.user.name)
        self.assertEqual(str(addr), addr.address_line1)
        self.assertEqual(str(gig), gig.title)
        self.assertEqual(str(edu), f'{edu.degree} from {edu.university}')
        
    
    @patch('uuid.uuid4')
    def test_path_of_uploaded_image(self, mock_uuid):

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_path_generator(None, 'myimage.jpg')

        expected_path = f'uploads/freelancer/{uuid}.jpg'

        self.assertEqual(file_path, expected_path)