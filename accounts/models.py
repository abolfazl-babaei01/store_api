from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from .managers import CustomUserManager
from utils.validators import phone_regex

import random
import string


# Create your models here.

def generate_random_otp_code():
    return ''.join(random.choices(string.digits, k=6))


class OTP(models.Model):
    phone_number = models.CharField(max_length=11, validators=[phone_regex, ])
    otp_code = models.CharField(max_length=6, default=generate_random_otp_code())
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"OTP for {self.phone_number}"

    def regenerate_otp(self):
        """
        Generate new OTP code and save it to database.
        """
        self.otp_code = generate_random_otp_code()
        self.save()

    def valid_delay(self):
        """
        Checks if at least 3 minutes have passed since the last OTP generation.
        """
        if self.created_at and now() <= self.created_at + timedelta(minutes=3):
            return False

        self.created_at = now()
        self.save()
        return True

    def is_otp_valid(self, otp):
        """
        Verifies if the provided OTP matches the generated code and
        ensures it has not expired (valid for up to 5 minutes).
        """
        if self.otp_code == str(otp) and now() <= self.created_at + timedelta(minutes=5):
            return True
        return False

    def send_sms_otp(self):
        """
        send sms to user phone number
        """
        print(f"Otp code {self.otp_code} To {self.phone_number}")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    custom user model
    """
    phone = models.CharField(max_length=11, unique=True, validators=[phone_regex, ])
    first_name = models.CharField(max_length=220, blank=True, null=True)
    last_name = models.CharField(max_length=220, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    street_or_residence = models.TextField()
    postal_code = models.CharField(max_length=10)



    def __str__(self):
        return f'{self.province} {self.city} {self.street_or_residence[:10]}'


    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

