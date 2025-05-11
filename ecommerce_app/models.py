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
  
  @property
  def imageUrl(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url
  
#Customer orders
class Order(models.Model): 
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  date_ordered = models.DateTimeField(auto_now_add = True)
  complete = models.BooleanField(default=False, null=True, blank=True)
  transaction_id = models.CharField(max_length=200, null=True)

  def __str__(self):
    return str(self.id)
  
  @property
  def get_cart_total(self):
    orderitems = self.items.all()
    total = sum([item.get_total for item in orderitems]) 
    return total
  
  @property
  def get_cart_items(self):
    orderitems = self.items.all()
    total = sum([item.quantity for item in orderitems])
    return total
  
  

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name = 'items', on_delete=models.CASCADE) 
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  date_added = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return str(self.product)

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total

  
  




# Create your models here.
