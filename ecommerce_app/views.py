from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecommerce_app.models import *
from ecommerce_app.forms import ProductForm
from django.http import JsonResponse
import json

def index(request):
  

  return render(request, 'ecommerce_app/index.html')


def signup(request):

  if request.method == 'POST':
    username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']

    myuser = User.objects.create_user(username, email, pass1)
    myuser.first_name = fname
    myuser.last_name = lname

    myuser.save()
    myuser.is_staff = False

    messages.success(request, "Your Account has been successfully created.")

    return redirect('signin')

  return render(request, 'ecommerce_app/signup.html')

def signin(request):

  if request.method == 'POST':
    username = request.POST['username']
    pass1 = request.POST['pass1']

    user = authenticate(username=username, password=pass1)

    if user is not None:
      login(request, user)
      fname = user.first_name
      return render(request, "ecommerce_app/index.html", {'fname': fname})

    else:
      messages.error(request, "Bad Credentials!")
      return redirect('ecommerce:index')

  return render(request, 'ecommerce_app/signin.html')

def signout(request):
  logout(request)
  messages.success(request, "Logged out Successfully!")
  return redirect('ecommerce:index')

def products(request):

  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user =request.user, complete=False)
    items = order.items.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

  result = Product.objects.all()

  context = {
    'result': result,
    'cartItems': cartItems,
  }

  return render(request, 'ecommerce_app/products.html', context)

def add_product(request):

  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('ecommerce:products')
  else:
    form = ProductForm()

  return render(request, 'ecommerce_app/add_product.html', {'form': form})

def details(request, product_id):
  result = get_object_or_404(Product, id=product_id)

  return render(request, 'ecommerce_app/details.html', {'result' : result})

def cart(request):

  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user =request.user, complete=False)
    items = order.items.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

  context = {
    'items': items,
    'order': order,
    'cartItems': cartItems,
  }
  return render(request, 'ecommerce_app/cart.html', context)

def checkout(request):
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user =request.user, complete=False)
    items = order.items.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

  context = {
    'items': items,
    'order': order,
    'cartItems': cartItems,
  }
  return render(request, 'ecommerce_app/checkout.html', context)

def updateItem(request):
  
  data = json.loads(request.body.decode('utf-8'))
  productId = data['productId']
  action = data['action']

  print('Action:', action)
  print('Product:', productId)

  user = request.user
  product = Product.objects.get(id=productId)

  order, created = Order.objects.get_or_create(user=user, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

  if action == 'add':
    orderItem.quantity += 1
  elif action == 'remove':
    orderItem.quantity -= 1

  orderItem.save()

  if orderItem.quantity <= 0:
    orderItem.delete()

  return JsonResponse('Item was added', safe=False)






# Create your views here