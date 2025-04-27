from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('products/', views.products, name='products'),
]