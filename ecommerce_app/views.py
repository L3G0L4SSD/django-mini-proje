from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecommerce_app.models import Product
from ecommerce_app.forms import ProductForm


def home(request):
  

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
      return redirect('home')

  return render(request, 'ecommerce_app/signin.html')

def signout(request):
  logout(request)
  messages.success(request, "Logged out Successfully!")
  return redirect('ecommerce:home')

def products(request):
  result = Product.objects.all()

  return render(request, 'ecommerce_app/products.html', {'result' : result})

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






# Create your views here