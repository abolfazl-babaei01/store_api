from django.contrib import admin
from .models import CustomUser, OTP, Address
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Register your models here.
@admin.register(OTP)
class AdminOtp(admin.ModelAdmin):
    list_display = ['phone_number']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ['phone']

    list_display = ['phone','first_name','last_name', 'is_active', 'is_staff']
    search_fields = ['phone']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'favorite_products')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)})
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'favorite_products')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)})
    )



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'province', 'city']

