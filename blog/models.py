from django.db import models

# Create your models here.
# class User(models.Model):
#     pass

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, )
    
    def __str__(self):
        return self.title