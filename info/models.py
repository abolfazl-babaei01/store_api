from django.db import models
from utils.validators import phone_regex


# Create your models here.


class AboutUs(models.Model):
    """
    Stores information about the 'About Us' section of the site.
    Includes title, description, and publication status.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'


class Privacy(models.Model):
    """
    Stores details about the site's privacy policy.
    Contains title, description, and publication status.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Privacy'
        verbose_name_plural = 'Privacies'


class TermsAndConditions(models.Model):
    """
    Represents the site's terms and conditions.
    Contains the title and full description of the rules.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'


class FAQ(models.Model):
    """
    Stores frequently asked questions and their answers.
    Includes a question title and corresponding answer.
    """
    question_title = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_title

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class ContactInfo(models.Model):
    """
    Holds contact details and social media IDs for the site.
    Includes whatsapp phone number, email, address, and social IDs.
    """
    telegram = models.CharField(max_length=255, blank=True, null=True)
    whatsapp_phone = models.CharField(max_length=11, blank=True, null=True, validators=[phone_regex])
    instagram =models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'Contact Information - {self.whatsapp_phone}'

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
