from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sale_price', 'rating', 'review_count')
    search_fields = ('name',)