from django.contrib import admin
from .models import Order,Item
# Register your models here.
class CartAdmin(admin.ModelAdmin):
  list_display=['order_id','ordered_at']

class CartItemAdmin(admin.ModelAdmin):
  list_display=['meal','order','number','is_active']

admin.site.register(Order,CartAdmin)
admin.site.register(Item,CartItemAdmin)