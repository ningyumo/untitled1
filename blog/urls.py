from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<tag>/', views.blog_list_with_type, name='blog_list_with_type'),
    path('detail/<pk>/', views.blog_detail, name='blog_detail'),
]