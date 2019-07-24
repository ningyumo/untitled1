from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from PIL import Image
import string
import random
import uuid
import os
import json

from .forms import RegisterForm, LoginForm, ChangeNickNameForm, ChangeEmailForm, ChangePasswordForm, FindPasswordForm
from .models import VerifyCode, Profile
from collection.models import Collection
from comment.models import Comment
from .forms import AvatarUploadForm


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
    upload_avatar_form = AvatarUploadForm

    def get_change_nick_name_form(self):
        return {'change_nick_name_form': self.change_nick_name_form}

    def get_change_email_form(self):
        return {'change_email_form': self.change_email_form}

    def get_change_password_form(self):
        return {'change_password_form': self.change_password_form}

    def get_upload_avatar(self):
        return {'upload_avatar_form': self.upload_avatar_form}

    # 个人信息
    def get_profile_information(self):
        profile = self.model.objects.get(user=self.request.user)
        return {'profile': profile}

    # 我的收藏
    def get_collection(self):
        collections_list = Collection.objects.filter(collector=self.request.user)

        collections = []
        for collection in collections_list:
            model = collection.content_type.model_class()
            object = model.objects.get(pk=collection.object_id)
            collections.append(object)
        return collections

    def get_comment(self):
        content_type = ContentType.objects.get(model='blog')
        comments = Comment.objects.filter(creater=self.request.user, content_type=content_type)
        return comments

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context.update(self.get_profile_information())
        context.update(self.get_change_nick_name_form())
        context.update(self.get_change_email_form())
        context.update(self.get_change_password_form())
        context.update(self.get_upload_avatar())
        context['collections'] = self.get_collection()
        context['comments'] = self.get_comment()
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


# 头像处理
def ajax_avatar_upload(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            img = request.FILES['avatar']  # 获取上传图片
            data = request.POST['avatar_data']  # 获取 ajax 返回图片坐标

            current_avatar = user_profile.avatar
            cropped_avatar = crop_image(current_avatar, img, data, user.id)
            user_profile.avatar = cropped_avatar  # 保存头像
            user_profile.save()
            data = {'result': user_profile.avatar.url}
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'msg': '请上传图片'})
    return redirect(reverse('accounts:profile'))


# 头像处理
def crop_image(current_avatar, file, data, uid):
    # 随机生成新的图片名
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # 自定义存储路径
    cropped_avatar = os.path.join(str(uid), 'avatar', file_name)
    # 相对根目录路径
    file_path = os.path.join('media', str(uid), 'avatar', file_name)
    # 获取 ajax 发送的裁剪参数 data，先用 json 解析
    coords = json.loads(data)
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片，压缩尺寸为400 * 400
    img = Image.open(file)
    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((200, 200), Image.ANTIALIAS).rotate(t_rotate)

    directory = os.path.dirname(file_path)
    if os.path.exists(directory):
        crop_im.save(file_path)
    else:
        os.makedirs(directory)
        crop_im.save(file_path)
    # # 如果头像不是默认头像，删除老头像图片，节省空间
    # if not current_avatar == os.path.join('avatar', 'default.jpg'):
    #     current_avatar_path = os.path.join('media', str(uid), 'avatar', os.path.basename(current_avatar.url))
    #     os.remove(current_avatar_path)
    return cropped_avatar