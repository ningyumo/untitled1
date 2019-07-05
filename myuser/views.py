from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import ContextMixin, View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
import string
import random
from importlib import import_module
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .models import VerifyCode


# 注册
class MyRegisterForm(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'my_user/register.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password_2']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            login(self.request, user)
            return redirect(self.success_url)


my_register = MyRegisterForm.as_view()


# 登陆
class LoginView(FormView):
    success_url = reverse_lazy('home')
    form_class = LoginForm
    template_name = 'my_user/login.html'

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return self.success_url

    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        return super().form_valid(form)


my_login = LoginView.as_view()


# 登出
def my_logout(request):
    logout(request)
    data = {}
    data['status'] = 'SUCCESS'


# 发邮件Mixin
def my_send_email(request):
    to = request.GET.get('to')
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    VerifyCode.objects.create(email=to, verify_code=code)

    send_mail(
        '验证邮箱',
        "您的验证码为：%s。验证码 10 分钟内有效。" % code,
        '653056889@qq.com',
        [to],
        fail_silently=False,
    )

    request.session['code_for_%s' % to] = code
    return JsonResponse({'status': 'SUCCESS'})