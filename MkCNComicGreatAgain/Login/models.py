from django.db import models

# Create your models here.

class User(models.Model):
    UserName = models.CharField(max_length=40) #用户名，最长40个字符
    PassWord = models.CharField(max_length=20) #密码，最长20个字符
    Email = models.CharField()
    class Meta:
        ording = ('created',)