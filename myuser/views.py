from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import string
import random

from .forms import RegisterForm, LoginForm, ChangeNickNameForm, ChangeEmailForm, ChangePasswordForm, FindPasswordForm
from .models import VerifyCode, Profile


# 注册
class MyRegisterFormView(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'my_user/register.html'

    def get_form_kwargs(self):
        kwargs = super(MyRegisterFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password_2']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user)
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            login(self.request, user)
            return redirect(self.success_url)


my_register = MyRegisterFormView.as_view()


# 登陆
class LoginView(FormView):
    success_url = reverse_lazy('home')
    form_class = LoginForm
    template_name = 'my_user/login.html'

    def get_success_url(self):
        success_url = self.request.GET.get('next', self.success_url)
        if success_url.startswith('/accounts/register') or success_url.startswith('/accounts/login'):
            return self.success_url
        else:
            return success_url

    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        self.request.session['%s_login' % self.request.user.username] = True
        self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)


my_login = LoginView.as_view()


# 登出
def my_logout(request):
    logout(request)
    request.session.flush()
    return redirect(reverse('home'))


# 发邮件
def my_send_email(request):
    action = request.GET.get('action')
    to = request.GET.get('to')
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    VerifyCode.objects.create(email=to, verify_code=code, action=action)

    send_mail(
        '验证邮箱',
        "您的验证码为：%s。验证码 10 分钟内有效。" % code,
        '653056889@qq.com',
        [to],
        fail_silently=False,
    )

    request.session['code_for_%s_by_%s' % (action, to)] = code
    return JsonResponse({'status': 'SUCCESS'})


# 个人中心
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    model = Profile
    template_name = 'my_user/profile.html'
    change_nick_name_form = ChangeNickNameForm
    change_email_form = ChangeEmailForm
    change_password_form = ChangePasswordForm

    def get_change_nick_name_form(self):
        return {'change_nick_name_form': self.change_nick_name_form}

    def get_change_email_form(self):
        return {'change_email_form': self.change_email_form}

    def get_change_password_form(self):
        return {'change_password_form': self.change_password_form}

    # 个人信息
    def get_profile_information(self):
        profile = self.model.objects.get(user=self.request.user)
        return {'profile': profile}

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context.update(self.get_profile_information())
        context.update(self.get_change_nick_name_form())
        context.update(self.get_change_email_form())
        context.update(self.get_change_password_form())
        return context


profile = ProfileView.as_view()


# 修改昵称
@method_decorator(login_required, name='dispatch')
class ChangeNickNameview(FormView):
    form_class = ChangeNickNameForm
    success_url = None
    template_name = None
    data = {}

    def form_valid(self, form):
        nick_name = form.cleaned_data['nick_name']
        Profile.objects.filter(user=self.request.user).update(nick_name=nick_name)
        self.data['status'] = 'SUCCESS'
        return JsonResponse(self.data)

    def form_invalid(self, form):
        self.data['status'] = 'ERRORS'
        return JsonResponse(self.data)


change_nick_name = ChangeNickNameview.as_view()


# 修改邮箱
@method_decorator(login_required, name='dispatch')
class ChangeEmailView(FormView):
    form_class = ChangeEmailForm
    template_name = None
    success_url = None
    data = {}

    def get_form_kwargs(self):
        kwargs = super(ChangeEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.save()
        self.data['status'] = 'SUCCESS'
        return JsonResponse(self.data)

    def form_invalid(self, form):
        self.data['status'] = form.cleaned_data['status']
        return JsonResponse(self.data)


change_email = ChangeEmailView.as_view()


# 修改密码
@method_decorator(login_required, name='dispatch')
class ChangePasswordFormView(FormView):
    form_class = ChangePasswordForm
    success_url = None
    template_name = None
    data = {}

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password_1'])
        user.save()
        self.data['status'] = 'SUCCESS'
        return JsonResponse(self.data)

    def form_invalid(self, form):
        self.data['status'] = form.cleaned_data['status']
        return JsonResponse(self.data)


change_password = ChangePasswordFormView.as_view()


# 找回密码
class FindPasswordFormView(FormView):
    form_class = FindPasswordForm
    template_name = 'my_user/find_password.html'
    success_url = reverse_lazy('accounts:login')

    def get_form_kwargs(self):
        kwargs = super(FindPasswordFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        password = form.cleaned_data['new_password_1']
        print(password)
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return redirect(self.get_success_url())
    

find_password = FindPasswordFormView.as_view()




