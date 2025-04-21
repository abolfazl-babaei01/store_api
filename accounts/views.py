from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (OTPRequestSerializer, OTPVerifySerializer, UserProfileSerializer, ResetPasswordSerializer,
                          ChangePhoneNumberSerializer,
                          AddressSerializer)
from .models import CustomUser, Address


# Create your views here.


class UserProfileDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    """
    API view to update the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ViewSet):
    """
       A viewset for managing addresses. Supports list, create, retrieve, update, and delete.
    """

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        if address.user != request.user:
            return Response({'message': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        if address.user != request.user:
            return Response(
                {'message': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN)
        serializer = AddressSerializer(instance=address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        if address and address.user == request.user:
            address.delete()
            return Response({'message': 'Address deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'You do not have permission to perform this action.'},
                        status=status.HTTP_403_FORBIDDEN)


class OTPRequestView(APIView):
    """
    API View for OTP Request and receive a OTP code.

    This view handles POST requests to generate and send an OTP code
    to the provided phone number for authentication or verification purposes.

    """

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Otp Code sent Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    """
    This view handles POST requests to verify the provided OTP and, upon successful
    verification, generates and returns JWT tokens (access and refresh tokens) for the user.
    """

    def create_token_response(self, user):
        """
         Generate JWT tokens for the authenticated user.
        :param user: The authenticated user instance.
        :return: A dictionary containing the refresh and access tokens.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.create_token_response(user))


class ResetPasswordView(APIView):
    """
    This View handles POST requests to reset password of a user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "password has ben reset successfully"}, status=status.HTTP_200_OK)


class ChangePhoneNumberView(generics.GenericAPIView):
    """
    This View handles POST requests to change the phone number of a user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your Phone Number Successfully Changed!'}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
