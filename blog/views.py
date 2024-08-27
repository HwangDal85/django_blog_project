# blog/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:list')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostUpdateView(UpdateView):
    model = Post
    context_object_name = 'post_update'
    form_class = PostForm
    success_url = reverse_lazy('blog:list')


class PostDeleteView(DeleteView):
    model = Post