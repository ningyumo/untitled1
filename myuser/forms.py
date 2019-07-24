from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import VerifyCode, Profile
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
    verify_code = forms.CharField(min_length=6,
                                  label='请输入验证码',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

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

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code']
        to = self.cleaned_data['email']
        session_verify_code = self.request.session['code_for_%s_by_%s' % ('register', to)]
        if session_verify_code != verify_code:
            raise forms.ValidationError("验证码错误")
        else:
            v = VerifyCode.objects.filter(email=to, action='register').update(used=True)
            del self.request.session['code_for_%s_by_%s' % ('register', to)]
        return verify_code


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
        print(username_or_email)
        password = self.cleaned_data['password']
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError("用户名或密码错误")
                else:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            else:
                raise forms.ValidationError("用户名或密码错误")
        else:
            self.cleaned_data['user'] = user
            return self.cleaned_data


# 修改昵称表单
class ChangeNickNameForm(forms.Form):
    nick_name = forms.CharField(max_length=100,
                                label='请输入昵称',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                }))

    def clean_nick_name(self):
        nick_name = self.cleaned_data['nick_name']
        if Profile.objects.filter(nick_name=nick_name).exists():
            raise forms.ValidationError('昵称已存在')
        return nick_name


# 修改邮箱表单
class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='请输入邮箱',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                             }))
    verify_code = forms.CharField(min_length=6,
                                  label='请输入验证码',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data['email']
        verify_code = self.cleaned_data['verify_code']
        # 验证邮箱是否存在
        if User.objects.filter(email=email).exists():
            self.cleaned_data['status'] = 'EMAIL_EXIST'
            raise forms.ValidationError('该邮箱已存在')

        # 验证验证码是否正确
        session_verify_code = self.request.session.get('code_for_%s_by_%s' % ('change_email', email))
        if session_verify_code != verify_code:
            self.cleaned_data['status'] = 'VERIFY_CODE_ERRORS'
            raise forms.ValidationError("验证码错误")
        else:
            v = VerifyCode.objects.filter(email=email, action='change_email').update(used=True)
            del self.request.session['code_for_%s_by_%s' % ('change_email', email)]
        print(self.cleaned_data)
        return self.cleaned_data


# 修改密码表单
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='请输入旧密码',
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                   }))
    new_password_1 = forms.CharField(label='请输入新密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={
                                         'class': 'form-control',
                                     }))
    new_password_2 = forms.CharField(label='请再次输入新密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={
                                         'class': 'form-control',
                                     }))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        username = self.request.user.username
        user = authenticate(username=username, password=old_password)
        if user is None:
            self.cleaned_data['status'] = 'OLD_PASSWORD_ERROR'
            raise forms.ValidationError('旧密码输入错误')
        return old_password

    def clean(self):
        new_password_1 = self.cleaned_data['new_password_1']
        new_password_2 = self.cleaned_data['new_password_2']


        if new_password_1 != new_password_2:
            self.cleaned_data['status'] = 'NEW_PASSWORD_ERROR'
            raise forms.ValidationError('新密码输入不一致')
        return self.cleaned_data


# 找回密码表单
class FindPasswordForm(forms.Form):
    email = forms.CharField(label='请输入邮箱',
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                            }))
    verify_code = forms.CharField(min_length=6,
                                  label='请输入验证码',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_password_1 = forms.CharField(label='请输入新密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={
                                         'class': 'form-control',
                                     }))
    new_password_2 = forms.CharField(label='请再次输入新密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={
                                         'class': 'form-control',
                                     }))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(FindPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data['email']
        verify_code = self.cleaned_data['verify_code']
        new_password_1 = self.cleaned_data['new_password_1']
        new_password_2 = self.cleaned_data['new_password_2']


        # 验证密码
        if new_password_1 != new_password_2:
            raise forms.ValidationError('新密码输入不一致')

        # 验证邮箱
        session_verify_code = self.request.session.get('code_for_%s_by_%s' % ('find_password', email))
        if session_verify_code != verify_code:
            raise forms.ValidationError("验证码错误")
        else:
            v = VerifyCode.objects.filter(email=email, action='find_password').update(used=True)
            del self.request.session['code_for_%s_by_%s' % ('find_password', email)]


        return self.cleaned_data


# 上传头像表单
class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': "avatar-input img-thumbnail",
        'id': "avatarInput" ,
        'type': 'file',
    }))


