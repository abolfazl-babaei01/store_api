from django.contrib import admin
from .models import Category, Product, ProductGallery, ProductFuture, ProductComment
from django.utils.html import mark_safe

# Register your models here.

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductFutureInline(admin.TabularInline):
    model = ProductFuture
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_editable = ('parent', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'off', 'new_price', 'price', 'show_image']
    inlines = [ProductGalleryInline, ProductFutureInline]

    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50px;" height="50px" />')


    show_image.short_description = 'Image'


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'status']