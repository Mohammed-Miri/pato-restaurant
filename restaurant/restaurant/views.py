from django.shortcuts import render
from meals.models import Meal, Review

from posts.models import Post
# from store.models import Product

def home(request):
  posts = Post.objects.all().order_by('-date_time')[:3]
  reviews = Review.objects.all()
  context = {
    'posts' : posts,
    'reviews' : reviews,
  }
  return render(request,'home.html',context)

def menu(request):
  return render(request,'menu/menu.html')

def about(request):
  return render(request,'about/about.html')

