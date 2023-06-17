from django.db import models
from django.urls import reverse
from django.db.models import Count
from customers.models import Accounts

# Create your models here.
class Post(models.Model):
  title= models.CharField(max_length= 250)
  image = models.ImageField(null=True,blank= True ,upload_to= "photos/categorires")
  short_description =  models.TextField(max_length= 300,null=True,blank=True)
  description= models.TextField(max_length= 100000)
  slug= models.SlugField(max_length= 250, unique= True,allow_unicode=True)
  date= models.DateField(auto_now_add= True)
  date_time = models.DateTimeField(auto_now_add=True)
  update_at = models.DateField(auto_now=True)

  class Meta:
      db_table= 'posts'
      verbose_name = 'post'
      verbose_name_plural = 'posts'
      
  def __str__(self):
    return self.title
  
  def get_url(self):
        return reverse('blog_detail',args=[self.slug])
      
  def countReview(self):
        comments = Comment.objects.filter(post=self, status=True).aggregate(count=Count('id'))
        count = 0
        if comments['count'] is not None:
            count = int(comments['count'])
        return count
      

# Create your models here.
class Comment(models.Model):
      ip = models.CharField(max_length=20,blank=True)
      status = models.BooleanField(default=True)
      subject = models.CharField(max_length=100,blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      description= models.TextField(max_length= 250)
      post = models.ForeignKey(Post, on_delete=models.CASCADE)
      customer = models.ForeignKey(Accounts, on_delete=models.CASCADE)

      class Meta:
            db_table= 'comments'
            verbose_name = "comment"
            verbose_name_plural = "comments"

      def __str__(self):
        return self.subject

