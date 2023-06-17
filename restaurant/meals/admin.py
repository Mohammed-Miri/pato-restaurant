from django.contrib import admin
from .models import Review,Variation,Meal
# Register your models here.
admin.site.register(Review)

class MealAdmin(admin.ModelAdmin):
  list_display = ('name','price','category','modified_date','is_availabel')
  prepopulated_fields = {'slug': ('name',)}
admin.site.register(Meal,MealAdmin)

class VariationAdmin(admin.ModelAdmin):
  list_display = ('product','variation_category' ,'variation_value','is_active')
  list_editable = ('is_active',)
  list_filter = ('product','variation_category' ,'variation_value')
admin.site.register(Variation,VariationAdmin)