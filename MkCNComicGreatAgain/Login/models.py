from django.db import models

# Create your models here.


class User(models.Model):
    # 用户名，最长40个字符
    username = models.CharField(max_length=40)
    # 密码，最长20个字符
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=128)
    active_email = models.BooleanField(default=False)

    class Meta:
        ording = ('created',)