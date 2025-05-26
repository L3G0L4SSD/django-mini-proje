import csv
from django.http import HttpResponse
from django.contrib import admin
from ecommerce_app.models import *
from django.urls import path
from django.template.response import TemplateResponse


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'stock', 'total_sold')
    actions = ['export_products_sold_csv']

    def changelist_view(self, request, extra_context=None):
      extra_context = extra_context or {}
      extra_context['sales_report_url'] = 'sales-report'
      return super().changelist_view(request, extra_context=extra_context)

    def total_sold(self, obj):
        return sum(item.quantity for item in obj.orderitem_set.filter(order__complete=True))
    total_sold.short_description = 'Total Sold'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-report/', self.admin_site.admin_view(self.sales_report_view), name='sales-report'),
        ]
        return custom_urls + urls
    
    def sales_report_view(self, request):
        products = Product.objects.all()
        labels = [p.name for p in products]
        data = [self.total_sold(p) for p in products]
        context = dict(
            self.admin_site.each_context(request),
            labels=labels,
            data=data,
        )
        return TemplateResponse(request, "admin/sales_report.html", context)
    
    

    def export_products_sold_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_sold_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Product Name', 'Price', 'Stock', 'Total Sold'])
        for product in queryset:
            writer.writerow([
                product.name,
                product.price,
                product.stock,
                self.total_sold(product)
            ])
        return response
    export_products_sold_csv.short_description = "Export Products Sold as CSV"

admin.site.register(Order) 
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.site_header = "E-commerce Admin"