from django.db import models
from customers.models import Accounts

from meals.models import Meal, Variation
# Create your models here.
class Order(models.Model):
  order_id = models.CharField(max_length=250,blank=True)
  ordered_at= models.DateTimeField(auto_now_add= True)
  class Meta:
    db_table= 'orders'
    verbose_name = 'order'
    verbose_name_plural = 'orders'

  def __str__(self):
      return self.order_id


class Item(models.Model):
    number= models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    customer = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table= 'items'
        verbose_name = 'item'
        verbose_name_plural = 'items'
    
    def sub_total(self):
        return self.meal.price * self.number
    
    def __unicode__(self):
        return self.meal