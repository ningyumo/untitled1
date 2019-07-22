from django.urls import path
from . import views

app_name = 'collection'
urlpatterns = [
    path('collect/', views.collect, name='collect'),
]