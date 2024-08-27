from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator

def home(request):
    recent_posts = Post.objects.order_by('-created_date')[:5]
    return render(request, 'blog/home.html', {'recent_posts': recent_posts})

def post_list(request):
    post_list = Post.objects.all().order_by('-created_date')
    paginator = Paginator(post_list, 10)  # 페이지당 10개 게시글

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/post_list.html', {'posts': posts})