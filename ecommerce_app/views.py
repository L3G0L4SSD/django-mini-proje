from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecommerce_app.models import *
from ecommerce_app.forms import ProductForm
from django.http import JsonResponse
import json
import datetime

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

    return redirect('ecommerce:signin')

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
    query = request.GET.get('q', '')
    if query:
        result = Product.objects.filter(name__icontains=query)
    else:
        result = Product.objects.all()

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

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

# def cart(request):

#   if request.user.is_authenticated:
#     order, created = Order.objects.get_or_create(user =request.user, complete=False)
#     items = order.items.all()
#     cartItems = order.get_cart_items
#   else:
#     items = []
#     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#     cartItems = order['get_cart_items']

#   context = {
#     'items': items,
#     'order': order,
#     'cartItems': cartItems,
#   }
#   return render(request, 'ecommerce_app/cart.html', context)

def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.items.all()
        cartItems = order.get_cart_items
    else:
        # Handle cookie cart
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except:
            cart = {}

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0

        for product_id in cart:
            try:
                quantity = cart[product_id]['quantity']
                product = Product.objects.get(id=product_id)
                total = product.price * quantity

                order['get_cart_total'] += total
                order['get_cart_items'] += quantity

                item = {
                    'product': product,
                    'quantity': quantity,
                    'get_total': total,
                }
                items.append(item)
                cartItems += quantity
            except:
                pass

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'ecommerce_app/cart.html', context)

def checkout(request):

  if not request.user.is_authenticated:
        messages.info(request, "You must login to proceed to checkout.")
        return redirect('ecommerce:signin')
  
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user =request.user, complete=False)
    items = order.items.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items':0, 'shipping': False}
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
    quantity = int(data.get('quantity', 1))  # <-- Make sure this line exists!

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += quantity
    elif action == 'remove':
        orderItem.quantity -= quantity

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'success': 'Item was added'})


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
            order.save()

            # Decrease stock for each product in the order
            for item in order.items.all():
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    # Handle out-of-stock scenario
                    messages.error(request, f"Not enough stock for {product.name}.")
                    return JsonResponse('Not enough stock', safe=False)
                    pass

            if order.shipping == True:
                ShippingAddress.objects.create(
                    user=request.user,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )
    return JsonResponse('Payment completed', safe=False)







# Create your views here