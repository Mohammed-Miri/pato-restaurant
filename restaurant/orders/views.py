from django.shortcuts import get_object_or_404, redirect, render
from .models import Item
from meals.models import Meal, Variation
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def cart(request, total=0, number=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Item.objects.filter(customer=request.user, is_active=True)
        else:
            cart = Order.objects.get(order_id=_cart_id(request))
            cart_items = Item.objects.filter(order=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.meal.price * cart_item.number)
            number += cart_item.number
        tax = (2 * total)/100
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'number': number,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product = Meal.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = Item.objects.filter(meal=product, customer=current_user).exists()
        if is_cart_item_exists:
            cart_item = Item.objects.filter(meal=product, customer=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Item.objects.get(meal=product, id=item_id)
                item.number += 1
                item.save()

            else:
                item = Item.objects.create(meal=product, number=1, customer=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Item.objects.create(
                meal = product,
                number = 1,
                customer = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Order.objects.get(order_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Order.DoesNotExist:
            cart = Order.objects.create(
                order_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = Item.objects.filter(meal=product, order=cart).exists()
        if is_cart_item_exists:
            cart_item = Item.objects.filter(meal=product, order=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Item.objects.get(meal=product, id=item_id)
                item.number += 1
                item.save()

            else:
                item = Item.objects.create(meal=product, number=1, order=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Item.objects.create(
                meal = product,
                number = 1,
                order = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Meal, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Item.objects.get(meal=product, customer=request.user, id=cart_item_id)
        else:
            cart = Order.objects.get(order_id=_cart_id(request))
            cart_item = Item.objects.get(meal=product, order=cart, id=cart_item_id)
        if cart_item.number > 1:
            cart_item.number -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Meal, id=product_id)
    if request.user.is_authenticated:
        cart_item = Item.objects.get(meal=product, customer=request.user, id=cart_item_id)
    else:
        cart = Order.objects.get(order_id=_cart_id(request))
        cart_item = Item.objects.get(meal=product, order=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



@login_required(login_url='login')
def checkout(request, total=0, number=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Item.objects.filter(customer=request.user, is_active=True)
        else:
            cart = Order.objects.get(order_id=_cart_id(request))
            cart_items = Item.objects.filter(order=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.meal.price * cart_item.number)
            number += cart_item.number
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'number': number,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'accounts/checkout.html', context)