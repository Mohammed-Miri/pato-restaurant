from multiprocessing import AuthenticationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from customers.forms import RegistrationForm
from customers.models import Accounts
from django.core.mail import EmailMessage
from django.contrib import messages , auth
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from orders.models import Item
from meals.models import Meal
from django.shortcuts import get_object_or_404
from orders.models import Order
from orders.views import _cart_id
# Create your views here.
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      phone_number = form.cleaned_data['phone_number']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      username = email.split("@")[0]
      user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
      user.phone_number = phone_number
      user.is_active = True
      user.save()
      messages.success(request,'Registration Successfully')
      return redirect('home')
  else:
    form = RegistrationForm()
  context = {
    'form' : form
  }
  return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
          try:
            cart= Order.objects.get(order_id=_cart_id(request))
            is_cart_item_exists = Item.objects.filter(order=cart).exists()
            if is_cart_item_exists:
              cart_item = Item.objects.filter(order=cart)
              product_variation = []
              for item in cart_item:
                variation = item.variations.all()
                product_variation.append(variation)
              cart_item = Item.objects.filter(customer=user)
              ex_var_list = []
              id = []
              for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
              for pr in product_variation:
                if pr in ex_var_list:
                  index = ex_var_list.index(pr)
                  item_id = id[index]
                  item = Item.objects.get(id=item_id)
                  item.number +=1
                  item.customer = user
                  item.save()
                else:
                  item = Item.objects.filter(order=cart)
                  for item in cart_item:
                    item.customer = user
                    item.save()
          except:
            pass
          auth.login(request, user)
          # messages.success(request, 'You are now logged in.')
          return redirect('home')
        else:
          messages.error(request,'Invalid Login')
          return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
  auth.logout(request)
  messages.success(request,'You Are Logout Now')
  return redirect('login')

@login_required(login_url = 'login')
def wishlist(request):
  products = Meal.objects.filter(user_wishlist=request.user)
  context = {
    'products' : products
  }
  return render(request,'accounts/user_wishlist.html',context)

@login_required(login_url = 'login')
def add_to_wishlist(request,id):
  product = get_object_or_404(Meal,id=id)
  if product.user_wishlist.filter(id=request.user.id).exists():
    messages.warning(request,'The' + product.name +'Was Removed From Wishlist')
    product.user_wishlist.remove(request.user)
  else:
    product.user_wishlist.add(request.user)
    messages.success(request,'The' + product.name +'Added To Wishlist Successfully')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
