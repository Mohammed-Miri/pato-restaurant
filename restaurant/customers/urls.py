from django.urls import path
from . import views

urlpatterns = [
    path('register/' ,views.register,name="register"),
    path('login/' ,views.login,name="login"),
    path('logout/' ,views.logout,name="logout"),
    path('wishlist/' ,views.wishlist,name="wishlist"),
    path('wishlist/add_to_wishlist/<int:id>' ,views.add_to_wishlist,name="add_to_wishlist"),
]
