from django.urls import path
from . import views

urlpatterns = [
    path('',views.gallery,name='gallery'),
    path('category/<slug:category_slug>/',views.gallery,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
    path('filter_by_price/', views.product_list, name='product_list'),
    path('filter_by_calory/', views.product_list2, name='product_list2'),
]