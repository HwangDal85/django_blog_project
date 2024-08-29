from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path("post/<int:pk>/comment_delete/", views.comment_delete, name="comment_delete"),

    path('signup/', views.user_signup, name="user_signup"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('profile/', views.user_profile, name="user_profile"),
    path('profile/update/', views.user_profile_update, name='user_profile_update'), 
    path('profile/pass_update/', views.change_password, name='user_pass_update'),
]
