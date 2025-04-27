from django.contrib import admin
from .models import AboutUs, Privacy, FAQ, TermsAndConditions, ContactInfo


# Register your models here.


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)


@admin.register(Privacy)
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'formated_created_date')

    def formated_created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    formated_created_date.short_description = 'Created at'


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'formated_created_date')

    def formated_created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    formated_created_date.short_description = 'Created at'


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('whatsapp_phone', 'email')
