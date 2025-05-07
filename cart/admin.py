from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.


class CaerItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'formated_date', 'cart_total_price']

    def formated_date(self, obj):
        return obj.created.strftime('%Y/%m/%d  %H:%M')

    formated_date.short_description = 'Create Date'

    inlines = [CaerItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass