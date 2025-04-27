from rest_framework import serializers
from .models import AboutUs, Privacy, FAQ, TermsAndConditions, ContactInfo


class AboutUsSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying About Us section content.
    """
    class Meta:
        model = AboutUs
        fields = ('title', 'description')


class PrivacySerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Privacy Policy content.
    """
    class Meta:
        model = Privacy
        fields = ('title', 'description')


class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying FAQs and their answers.
    """
    class Meta:
        model = FAQ
        fields = ('question_title', 'answer')


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Terms and Conditions content.
    """
    class Meta:
        model = TermsAndConditions
        fields = ('title', 'description')


class ContactInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying contact information and social links.
    """
    class Meta:
        model = ContactInfo
        fields = ('address', 'telegram', 'whatsapp_phone', 'instagram', 'email')
