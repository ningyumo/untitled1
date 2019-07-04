from django import forms
from django.contrib.auth.models import User


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=15,
                                min_length=6,
                                label='请输入密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=15,
                                min_length=6,
                                label='请再次输入密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次密码不一致')
        password = password1
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")

