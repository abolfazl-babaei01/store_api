from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['phone', 'first_name','last_name', 'is_staff', 'is_superuser', 'is_active']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and CustomUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain at least 11 digits')
        return phone


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['phone', 'first_name','last_name', 'is_staff', 'is_superuser', 'is_active']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and CustomUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain  11 digits')
        return phone
