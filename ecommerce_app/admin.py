from django.contrib import admin
from ecommerce_app.models import *
from django.utils.html import format_html




# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'description', 'stock', )

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.site_header = "E-commerce Admin"



    