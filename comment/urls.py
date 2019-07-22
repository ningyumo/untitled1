from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('submit/', views.comment_submit, name='comment_submit'),
    path('delete/<path:pk>/', views.comment_delete, name='comment_delete'),
]