from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.my_register, name='register'),
    path('register/sendemail/',views.my_send_email, name='sendmail'),
    path('logout/', views.my_logout, name='logout'),
    path('login/', views.my_login, name='login'),

]