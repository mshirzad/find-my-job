from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

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

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Address(models.Model):

    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    distrect = models.IntegerField()
    street = models.CharField(max_length=255)
    address_line = models.CharField(max_length=255)


class Profile(models.Model):

    PROFESSION_CHOICES = (
        ('Eng', 'Engineer'),
        ('Acc', 'Accountant'),
        ('Phy', 'Physician'),
        ('Tech', 'Technician'),
        ('Plu', 'Plumber'),
        ('Elect', 'Electrician'),
        ('Carp', 'Carpenter'),
        ('Phot','Photographer')
    ) 

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.IntegerField()
    profession = models.CharField(max_length=255, choices=PROFESSION_CHOICES)
    #image field must be added.
    ratings = models.FloatField(default=0)
    base_addr = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name