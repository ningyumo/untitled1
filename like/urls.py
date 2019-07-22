from django.urls import path
from . import views

app_name = 'like'
urlpatterns = [
    path('change/', views.like_change, name='like_change'),
]