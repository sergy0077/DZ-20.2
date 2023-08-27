from django.contrib import admin
from .models import Category, Product, Version, Contacts


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text')
    list_display_links = ('pk', 'title')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category')
    list_filter = ('category',)  # Фильтр по категориям
    search_fields = ('title', 'text',)  # Поля для поиска по названию и описанию


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'version_name')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'phone', )
    list_filter = ('address',)

