from django.urls import path
from . import views

urlpatterns = [
    path('',views.blog,name='blog'),
    path('<slug:post_slug>',views.blog_detail,name='blog_detail'),
    path('submit_post/<int:post_id>', views.submit_post, name='submit_post'),
]