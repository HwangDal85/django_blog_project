from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_create(request):
    if request.method == "POST": # Post요청 확인
        form = PostForm(request.POST) # PostFrom 인스턴스 생성 인자 전달
        if form.is_valid(): # 폼의 유효성
            post = form.save(commit=False) # Post객체 생성
            post.author = request.user  # 현재는 로그인 기능이 없으므로 나중에 구현
            post.save() #객체 저장
            return redirect('post_detail', pk=post.pk) # 새로 생성된 게시물의 상세 페이지로 리 디렉션 / post_detail URL 패턴에 새 게시물의 기본 키('pk')를 전달
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) # 이미 데이터베이스에 저장된 게시물을 수정 instance = post 기존 Post객체를 폼에 제공
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재는 로그인 기능이 없으므로 나중에 구현
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})