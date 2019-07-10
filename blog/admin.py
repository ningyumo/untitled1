from django.contrib import admin
from .models import Blog, BlogTag


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'creater', 'created_time', 'last_time']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time', 'last_time']



