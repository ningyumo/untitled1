from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogTag(models.Model):
    name = models.CharField(unique=True, max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    introduction = models.TextField(max_length=200)
    content = models.TextField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')  # 作者
    tag = models.ManyToManyField(BlogTag, related_name='blogs')

    created_time = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title











