from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.my_register, name='register'),  # 注册
    path('sendemail/', views.my_send_email, name='sendmail'),  # 发邮件
    path('logout/', views.my_logout, name='logout'),  # 退出
    path('login/', views.my_login, name='login'),  # 登陆
    path('profile/', views.profile, name='profile'),  # 个人中心
    path('profile/change/nickname/', views.change_nick_name, name='change_nick_name'),  # 修改昵称
    path('profile/change/email/', views.change_email, name='change_email'),  # 修改邮箱
    path('profile/change/password/', views.change_password, name='change_password'),  # 修改密码
    path('find/password/', views.find_password, name='find_password'),  # 找回密码
]