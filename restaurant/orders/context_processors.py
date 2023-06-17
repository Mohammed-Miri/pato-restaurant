from .models import Item
from .models import Order
from .views import _cart_id
def counter(request):
  cart_count = 0
  if 'admin' in request.path:
      return{}
  else:
    try:
      cart = Order.objects.filter(order_id=_cart_id(request))
      if request.user.is_authenticated:
        cart_items = Item.objects.all().filter(customer=request.user)
      else:
        cart_items = Item.objects.all().filter(order=cart[:1])
      for cart_item in cart_items:
        cart_count = cart_count + cart_item.number
    except Order.DoesNotExist:
      cart_count = 0
  return dict(cart_count=cart_count)