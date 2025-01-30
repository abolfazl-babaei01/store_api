from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['phone', 'total_price', 'is_paid', 'status', 'formating_created_date']
    list_editable = ['status']
    inlines = [OrderItemInline]

    def formating_created_date(self, obj):
        return obj.created.strftime('%Y/%m/%d | %H:%M')
    formating_created_date.short_description = 'Created'