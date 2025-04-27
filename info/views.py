from rest_framework import permissions, generics
from info.models import Privacy, AboutUs, FAQ, TermsAndConditions, ContactInfo
from info.serializers import AboutUsSerializer, PrivacySerializer, FAQSerializer, TermsAndConditionsSerializer, \
    ContactInfoSerializer


# Create your views here.


class AboutUsApiView(generics.ListAPIView):
    """
    API view to retrieve the About Us content.
    Only published About Us entries are returned.
    """
    serializer_class = AboutUsSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = AboutUs.objects.filter(is_published=True)


class PrivacyApiView(generics.ListAPIView):
    """
    API view to retrieve Privacy Policy content.
    Only published Privacy entries are returned.
    """
    serializer_class = PrivacySerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Privacy.objects.filter(is_published=True)


class FAQApiView(generics.ListAPIView):
    """
    API view to retrieve all Frequently Asked Questions.
    Returns a list of all available FAQs.
    """
    serializer_class = FAQSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = FAQ.objects.all()


class TermsAndConditionsApiView(generics.ListAPIView):
    """
    API view to retrieve Terms and Conditions content.
    Returns a list of all terms and conditions.
    """
    serializer_class = TermsAndConditionsSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = TermsAndConditions.objects.all()


class ContactInfoApiView(generics.ListAPIView):
    """
    API view to retrieve contact information and social media links.
    Returns available contact information entries.
    """
    serializer_class = ContactInfoSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = ContactInfo.objects.all()
