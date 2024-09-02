from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.paginator import Paginator
from .models import Post, Category, Comment, Tag
from .forms import PostForm, CommentForm, UserProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.views.generic.edit import FormMixin

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'recent_posts'
    queryset = Post.objects.order_by('-created_date')[:5]

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        selected_category = self.request.GET.get("category", "")
        selected_tag = self.request.GET.get("tag", "")

        posts = Post.objects.all()

        if q:
            posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if selected_category:
            posts = posts.filter(category_id=selected_category)
        if selected_tag:
            posts = posts.filter(tags__name__iexact=selected_tag)
        
        return posts.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get("category", "")
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get("tag", "")
        return context

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_object(self, queryset=None):
        try:
            return Post.objects.get(pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            return redirect('post_not_found')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        return redirect('post_detail', pk=comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post.view_count += 1
        post.save()
        context['form'] = self.get_form()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()  # Save ManyToMany field
        return redirect('post_detail', pk=post.pk)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()
        return redirect('post_detail', pk=post.pk)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class BlogTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__name__iexact=self.kwargs['tag'])

class TagSearchView(ListView):
    model = Post
    template_name = 'blog/tag_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        selected_tags = self.request.GET.getlist('tags')
        posts = Post.objects.all()
        if selected_tags:
            posts = posts.filter(tags__name__in=selected_tags).distinct()
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context

class PostNotFoundView(TemplateView):
    template_name = 'blog/post_not_found.html'

#==============================================================

class UserSignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/user_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        
        return response

class UserLoginView(FormView):
    template_name = 'accounts/user_login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super().form_valid(form)
    
class UserLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_profile.html'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'accounts/user_profile_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user

class UserPassUpdateView(LoginRequiredMixin, FormView):
    template_name = 'accounts/user_pass_update.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

#============================================================

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object.author:
            return super().delete(request, *args, **kwargs)
        return redirect(self.get_success_url())
