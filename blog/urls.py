# blog/urls.py
from django.urls import path
from blog.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete')
]