from django.contrib import admin
from ecommerce_app.models import Product
from django.utils.html import format_html




# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'description', 'stock', )
    