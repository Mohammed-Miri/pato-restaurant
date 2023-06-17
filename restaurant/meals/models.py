from django.db import models
from customers.models import Accounts
from django.urls import reverse
from django.db.models import Avg,Count
# Create your models here.
class Meal(models.Model):
    name= models.CharField(max_length= 250, unique= True)
    slug= models.SlugField(max_length= 250, unique= True,allow_unicode=True)
    price= models.IntegerField()
    image = models.ImageField(null=True,blank= True ,upload_to= "photos/meals")
    calories= models.IntegerField()
    ingredients= models.TextField(max_length= 1000, null= True, blank= True)
    category = models.ForeignKey('categories.Category',on_delete=models.CASCADE)
    is_availabel = models.BooleanField(default= True)
    created_date= models.DateTimeField(auto_now_add= True)
    modified_date= models.DateTimeField(auto_now= True)
    user_wishlist= models.ManyToManyField(Accounts,related_name="user_wishlist",blank=True)
    class Meta:
        db_table= 'meals'
        verbose_name = 'meal'
        verbose_name_plural = 'meals'
    
    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    def averageReview(self):
        reviews = Review.objects.filter(meal=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Review.objects.filter(meal=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    


# Create your models here.
class Review(models.Model):
      ip = models.CharField(max_length=20,blank=True)
      status = models.BooleanField(default=True)
      subject = models.CharField(max_length=100,blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      rating = models.FloatField()
      review= models.CharField(max_length= 250,blank=True)
      meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
      customer = models.ForeignKey(Accounts, on_delete=models.CASCADE)

      class Meta:
            db_table= 'reviews'
            verbose_name = 'review'
            verbose_name_plural = 'reviews'

      def __str__(self):
            return self.subject
        
    
class VariationManager(models.Manager):
    def hots(self):
        return super(VariationManager,self).filter(variation_category='hot',is_active=True)
    def types(self):
        return super(VariationManager,self).filter(variation_category='type',is_active=True)
    def sugars(self):
        return super(VariationManager,self).filter(variation_category='sugar',is_active=True)
    def nuts(self):
        return super(VariationManager,self).filter(variation_category='nut',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    
variation_category_choise = (
    ('hot','hot'),
    ('type','type'),
    ('sugar','sugar'),
    ('nut','nut'),
    ('size','size'),
)
class Variation(models.Model):
    product = models.ForeignKey(Meal,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length= 100,choices=variation_category_choise)
    variation_value = models.CharField(max_length= 100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()
    def __str__(self):
        return self.variation_value