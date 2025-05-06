from django.db import models
import datetime
from django.contrib.auth.models import User # or get_user_model() if custom user 


#All of our products 
class Product(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits = 8, decimal_places = 2)
  image = models.ImageField(upload_to='images/', null=True, blank=True)
  stock = models.IntegerField()
 

  def __str__(self):
    return self.name
  
#Customer orders
class Order(models.Model): 
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add = True)

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name = 'items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  




# Create your models here.
