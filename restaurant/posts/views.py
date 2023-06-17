from django.shortcuts import render
from posts.models import Comment, Post
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CommentForm

# Create your views here.
def blog(request):
  posts = Post.objects.all().order_by('-date_time')
  context = {
    'posts' : posts,
  }
  return render(request,'blog/blog.html',context)

def blog_detail(request,post_slug):
  try:
    single_blog = Post.objects.get(slug=post_slug)
    comments = Comment.objects.filter(post_id=single_blog.id,status=True)
  except Exception as e:
    raise e
  context = {
    'single_blog' : single_blog,
    'comments' : comments,
  }
  return render(request,'blog/blog-detail.html',context)


def submit_post(request, post_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            comments = Comment.objects.get(customer__id = request.user.id,post__id = post_id)
            form = CommentForm(request.POST, instance=comments)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except Comment.DoesNotExist:
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.subject = form.cleaned_data['subject']
                data.description = form.cleaned_data['description']
                data.ip = request.META.get('REMOTE_ADDR')
                data.post_id = post_id
                data.customer_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)