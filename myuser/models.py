from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog


# 个人信息
class Profile(models.Model):
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.user.username


# 验证码
class VerifyCode(models.Model):
    email = models.EmailField()
    verify_code = models.CharField(max_length=6)
    used = models.BooleanField(default=False)
    action = models.CharField(max_length=100)


