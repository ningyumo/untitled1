from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password_1 = forms.CharField(min_length=6,
                                 label='请输入密码',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_2 = forms.CharField(min_length=6,
                                 label='请再次输入密码',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    varify_code = forms.CharField(min_length=6,
                                  label='请输入验证码',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 != password_2:
            raise forms.ValidationError('两次密码不一致')
        return password_2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_varify_code(self):
        pass

# 登陆表单
class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=100,
                                        label='用户名或邮箱',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100,
                               label="密码",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        print(self.cleaned_data)
        print(username_or_email, password)
        user = authenticate(username=username_or_email, password=password)
        print(user)
        if user is None:
            if User.objects.filter(username='username_or_email').exists():
                username = User.objects.filter(username='username_or_email').username
                user = authenticate(email=username, password=password)
            if user is None:
                raise forms.ValidationError("用户名或密码错误")
        self.cleaned_data['user'] = user
        return self.cleaned_data