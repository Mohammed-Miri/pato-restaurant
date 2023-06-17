from django.shortcuts import get_object_or_404, render
from categories.models import Category
from orders.models import Item
from orders.views import _cart_id
from .models import Meal,Review
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def gallery(request,category_slug=None):
  categories = None
  meals = None
  reviews=0
  if category_slug !=None:
    categories = get_object_or_404(Category,slug=category_slug)
    meals = Meal.objects.filter(category = categories,is_availabel = True)
    paginator = Paginator(meals,200)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    product_count = meals.count()
    for meal in meals:
      reviews = Review.objects.filter(meal_id=meal.id,status=True)
  else:
    meals = Meal.objects.all().filter(is_availabel=True).order_by('id')
    paginator = Paginator(meals,9)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    for meal in meals:
      reviews = Review.objects.filter(meal_id=meal.id,status=True)
  product_count = meals.count()
  context = {
    'meals' : page_products,
    'reviews' : reviews,
    'product_count': product_count
  }
  return render(request,'gallery/gallery.html',context)





def product_detail(request,category_slug,product_slug):
  try:
    single_product = Meal.objects.get(category__slug=category_slug,slug=product_slug)
  except Exception as e:
    raise e

  reviews = Review.objects.filter(meal__id=single_product.id,status=True)
  context = {
    'single_product' : single_product,
    'reviews' : reviews,
  }
  return render(request,'gallery/product_detail.html',context)




def search(request,product_count=0):
    if 'keyword2' in request.GET:
        keyword = request.GET['keyword2']
        if keyword:
            meals = Meal.objects.filter(Q(ingredients__icontains = keyword) | Q(name__icontains = keyword))
            product_count = meals.count()
    context = {
        'meals': meals,
        'product_count': product_count,
    }
    return render(request,'gallery/gallery.html',context)

  
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(customer__id=request.user.id, meal__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.meal_id = product_id
                data.customer_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def product_list(request):
    products = Meal.objects.all()
    if request.method == 'POST':
        price_min = request.POST.get('price_min')
        price_max = request.POST.get('price_max')
        if price_min and price_max:
            products = products.filter(price__range=(price_min, price_max))
            product_count = products.count()
    return render(request, 'gallery/price.html', {'products': products,'product_count':product_count})
  
  
def product_list2(request):
    products = Meal.objects.all()
    if request.method == 'POST':
        calory_min = request.POST.get('calory_min')
        calory_max = request.POST.get('calory_max')
        if calory_min and calory_max:
            products = products.filter(calories__range=(calory_min, calory_max))
            product_count = products.count()
            
    return render(request, 'gallery/price.html', {'products': products,'product_count':product_count})
