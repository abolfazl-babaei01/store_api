from rest_framework import serializers
from rest_framework.fields import empty
from utils.validators import phone_regex
from django.contrib.auth import password_validation
from .models import OTP, CustomUser, Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model, Create new address for user
    """
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = ['id', 'user', 'province', 'city', 'postal_code', 'street_or_residence']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # add current user in to address
        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for user profile, managing personal details and read-only fields.
    """

    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'last_name', 'date_joined']
        extra_kwargs = {
            'phone': {'read_only': True},
            'date_joined': {'read_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class OTPVerificationBaseSerializer(serializers.Serializer):
    """
    Base serializer for verifying OTP codes with phone numbers and reset password and change phone number.
    Validates OTP and associates it with a phone number.
    """
    phone = serializers.CharField(max_length=11, validators=[phone_regex])
    otp = serializers.CharField(max_length=6)

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.otp_verification = None  # Initialize OTP verification instance

    def validate(self, data):
        otp = data.get("otp")
        phone = data.get("phone")

        try:
            otp_verification = OTP.objects.get(phone_number=phone)
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'message': 'invalid phone number or otp code'})

        # Check if the provided OTP is valid and has not expired
        if not otp_verification.is_otp_valid(otp) or not otp.isdigit():
            raise serializers.ValidationError({'message': 'invalid otp or expired otp'})

        self.otp_verification = otp_verification  # Initialize OTP verification instance
        return data


class OTPRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting OTP code.
    Response this serializer is OTP code for entered phone number.
    """
    phone = serializers.CharField(max_length=11, validators=[phone_regex])

    def create(self, validated_data):
        otp, created = OTP.objects.get_or_create(phone_number=validated_data["phone"])

        # Check the provided OTP if expired regenerate new OTP code for entered phone number
        if otp.valid_delay():
            otp.regenerate_otp()
            otp.send_sms_otp()
        else:
            raise serializers.ValidationError({'message': 'Your otp code has not expired'})
        return otp


class OTPVerifySerializer(OTPVerificationBaseSerializer):
    """
    Handles OTP verification and user creation.
    """

    password = serializers.CharField(
        write_only=True,
        max_length=8,
        required=False
    )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.filter(phone=validated_data["phone"]).first()

        if not user:
            if not password:
                raise serializers.ValidationError({'Error': 'password is required for registration'})

            # create new user
            user = CustomUser.objects.create_user(
                phone=validated_data.get('phone'),
                password=password)

        self.otp_verification.delete()  # Removed the used OTP instance
        return user


class ResetPasswordSerializer(OTPVerificationBaseSerializer):
    """
    Serializer for resetting a user's password using OTP verification.
    Inherits from `OTPVerificationBaseSerializer` to handle OTP validation.
    Validates the new password and updates the user's password upon successful OTP verification.
    """
    new_password = serializers.CharField()
    old_password = serializers.CharField()

    def get_user(self, data):
        user = CustomUser.objects.get(phone=data.get('phone'))
        if not user:
            raise serializers.ValidationError({'Error': 'user does not exist'})
        return user

    def validate(self, data):
        data = super().validate(data)
        user = self.get_user(data)



        password_validation.validate_password(data.get('new_password'))  # validate provided new password

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'Error': 'invalid old password'})

        return data

    def save(self):
        user = self.get_user(self.validated_data)

        user.set_password(self.validated_data["new_password"])  # hashed password and set for current user
        user.save()
        self.otp_verification.delete()  # Removed the used otp
        return user


class ChangePhoneNumberSerializer(OTPVerificationBaseSerializer):
    """
    Serializer for changing a user's phone number using OTP verification
    """

    def save(self):
        new_phone = self.validated_data['phone']
        user = self.context.get('request').user
        # check if entered phone number exists or not exists
        if CustomUser.objects.filter(phone=new_phone).first():
            raise serializers.ValidationError({'message': 'phone number already exists'})

        user.phone = new_phone
        user.save()
        self.otp_verification.delete()
        return user
