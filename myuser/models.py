from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    nick_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.user.username


class VerifyCode(models.Model):
    email = models.EmailField()
    verify_code = models.CharField(max_length=6)
    used = models.BooleanField(default=False)


