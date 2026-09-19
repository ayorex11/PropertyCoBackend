from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random
import pycountry

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            username=username,
            email=email,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Is Admin must have is_admin=True.')

        return self.create_user(username, email, password, **extra_fields)


def get_country_code_choices():
    return [(country.alpha_2, f"{country.name} (+{country.numeric})") for country in pycountry.countries]


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=50, unique=True)
    country_code = models.CharField(max_length=2, choices=get_country_code_choices(), default='US')
    CHOICES = (
      ('Agent', 'Agent'),
      ('User', 'User'),
      ('Admin', 'Admin'), #
      )
    account_type = models.CharField(max_length=20, choices=CHOICES, default='Agent')
    phone_number = models.CharField(max_length=25, blank=True, null=True, unique=True)
    member_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, null=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.member_id:
            while True:
                random_id = '24' + ''.join(str(random.randint(0, 9)) for _ in range(4))
                if not User.objects.filter(member_id=random_id).exists():
                    self.member_id = random_id
                    break
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email

    def __str__(self):
        return self.email
