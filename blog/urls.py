from django.urls import path
from .views import (
    HomeView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    BlogTagView, TagSearchView, PostNotFoundView,
    UserSignupView, UserLoginView, UserLogoutView, UserProfileView, UserProfileUpdateView, ChangePasswordView,
    CommentDeleteView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/tag-search/', TagSearchView.as_view(), name='tag_search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post-not-found/', PostNotFoundView.as_view(), name='post_not_found'),

    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('profile/pass_update/', ChangePasswordView.as_view(), name='user_pass_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
