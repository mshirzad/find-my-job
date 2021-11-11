import os, uuid

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

def image_path_generator(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'uploads/freelancer/', filename)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('You must have an Email Address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_freelancer = False

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Profile(models.Model):

    PROFESSION_CHOICES = (
        ('Eng', 'Engineer'),
        ('CS', 'Computer Scientist'),
        ('Gph Desg', 'Graphic Designer'),
        ('Web Dev', 'Web Developer'),
        ('Mobile Dev', 'Mobile App Developer'),
        ('Programmer', 'Programmer'),
        ('Acc', 'Accountant'),
        ('Phy', 'Physician'),
        ('Tech', 'Technician'),
        ('Plu', 'Plumber'),
        ('Elect', 'Electrician'),
        ('Carp', 'Carpenter'),
        ('Phot','Photographer')
    ) 
    REGEX_MSG = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    PHONE_NO_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=REGEX_MSG)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(validators=[PHONE_NO_REGEX], max_length=17) # validators should be a list
    profession = models.CharField(max_length=255, choices=PROFESSION_CHOICES)
    ratings = models.FloatField(default=0)
    bio = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(null=True, upload_to=image_path_generator)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, related_name='address')
    education = models.ForeignKey('Education', on_delete=models.CASCADE, blank=True, related_name='education')

    def __str__(self):
        return self.user.name


class Address(models.Model):

    address_line1 = models.CharField(max_length=512)
    address_line2 = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.address_line1


class Education(models.Model):

    DEGREE_CHOICES = (
        ('Diploma', 'Diploma'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('Phd', 'Phd')
    )

    degree = models.CharField(max_length=255, choices=DEGREE_CHOICES) 
    university = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    start_year = models.IntegerField()
    graduation_year = models.IntegerField()

    def __str__(self):
        return f'{self.degree} from {self.university}'


class Gig(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    min_price = models.DecimalField(max_digits=5, decimal_places=2)
    freelancer = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile')
    thumbnail = models.ImageField(upload_to=image_path_generator)
    thumbnail_2 = models.ImageField(null=True, upload_to=image_path_generator)
    thumbnail_3 = models.ImageField(null=True, upload_to=image_path_generator)

    def __str__(self):
        return self.title


# class Chat(models.Model):

#     ROOM_NAME_DEFAULT = Gigs.title
#     room_name = models.CharField(max_length=255, default=ROOM_NAME_DEFAULT)
#     sender = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date_time = models.DateTimeField()
#     attachement = models.FileField(blank=True)
#     message = models.CharField(max_length=1024)

#     def __str__(self):
#         return self.room_name