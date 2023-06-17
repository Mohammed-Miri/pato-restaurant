from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length= 250, unique= True)
    slug= models.SlugField(max_length= 250, unique= True,allow_unicode=True)
    image = models.ImageField(null=True,blank= True ,upload_to= "photos/categorires")
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)


    class Meta:
        db_table= 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    def __str__(self):
        return self.name