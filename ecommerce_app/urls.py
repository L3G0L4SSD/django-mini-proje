from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('home/signup/', views.signup, name='signup'),
    path('home/signin/', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('details/<int:product_id>/', views.details, name='details'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('order-history/', views.order_history, name='order_history'),
]