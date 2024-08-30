from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserProfileUpdateForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    recent_posts = Post.objects.order_by('-created_date')[:5]
    return render(request, 'blog/home.html', {'recent_posts': recent_posts})

def post_list(request):
    q = request.GET.get("q","")
    selected_category = request.GET.get("category","")

    posts = Post.objects.all()

    if q:
        posts = Post.objects.filter(title__icontains=q).order_by('-created_date')| Post.objects.filter(content__icontains=q).order_by('-created_date')
    if selected_category:
        posts = posts.filter(category_id=selected_category)
    
    posts = posts.order_by('-created_date')

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.all()

    return render(request, 'blog/post_list.html', {'posts': posts, "q":q, "categories":categories, "selected_category":selected_category})

def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return redirect('post_not_found')
    
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            message = form.cleaned_data["message"]
            c = Comment.objects.create(post=post, author=author, message=message)
            c.save()
    
    else:
        post.view_count += 1
        post.save()
    return render(
        request,
        "blog/post_detail.html",
        {"post":post, "form":form},
    )

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def blog_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "blog/post_list.html", {"posts":posts})

def post_not_found(request):
    return render(request, 'blog/post_not_found.html')
#===============================================

def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST.get("email", "")
        nickname = request.POST.get("nickname","")

        if not (username and password):
            return HttpResponse("이름과 패스워드는 필수입니다")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("이미 존재하는 사용자입니다")
        
        if email and User.objects.filter(email=email).exists():
            return HttpResponse("이미 존재하는 이메일입니다")


        user = User.objects.create_user(username, email, password)
        user.first_name = nickname
        user.save()


        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        return render(request, "accounts/user_signup.html")
    
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "accounts/user_login.html",
                {"error":"아이디, 또는 비밀번호가 틀렸습니다"},
            )
    else:
        return render(request, "accounts/user_login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def user_profile(request):
    return render(request, "accounts/user_profile.html", {"user": request.user})

@login_required
def user_profile_update(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/user_profile_update.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user_profile')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'accounts/user_pass_update.html', {'form': form})

#===========================================================

def comment_delete(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
    return redirect("post_detail", post.pk)