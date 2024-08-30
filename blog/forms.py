from django import forms
from .models import Post, Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name']
        labels = {
            'first_name': '닉네임',
        }