from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from Login.models import User
import re

def Password_Change(password):

    if len(password) < 8:
        return '密码少于8位数'
    elif password.isdigit() or password.isalpha():
        return '密码至少为字母与数字的结合'
    return '修改密码成功'
def Password_Find_Check(email, username):
    if username != '':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return '无此用户'
    elif email != '':
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return '无此用户'
    else:
        return '不能为空'
    return '已发送邮件'

def Register_Message_Check(email, username, password):
    # 验证邮箱
    if not re.match(r".*?@.*?\..*?", email):
        return '邮箱格式错误'
    if_email = User.objects.filter(email=email).first()
    if if_email:
        return '邮箱重复'
    # 验证用户名
    if_name = User.objects.filter(username=username).first()
    if username == '':
        return '用户名不能为空'
    if if_name:
        return '用户名重复'
    # 验证密码安全性（至少8位数并且包含数字字母）
    if len(password) < 8:
        return '密码少于8位数'
    elif password.isdigit() or password.isalpha():
        return '密码至少为字母与数字的结合'
    return '注册成功'


def Create_Token(username, email):

    idsfy = ts(settings.SECRET_KEY)
    data = {
        'username': username,
        'email': email,
    }
    # 生成isdangerous token
    token = idsfy.dumps(data).decode()
    return token


def Email_send(username, email, type=1):
    token = Create_Token(username, email)
    # 拼接邮件内容
    if type == 1:
        url = 'http://127.0.0.1:8000/Login/email/vary/?token=' + token
    if type == 2:
        url = 'http://127.0.0.1:8000/Login/email/find/?token=' + token

    url_str = '<a href=' + url + '>click to verify ur email</a>'

    email_url = email
    # 发送验证邮件
    send_mail(subject='hermit email active', message=url_str, from_email=settings.EMAIL_FROM,
              recipient_list=[email_url], html_message=url_str)

def From_token(receive_token):

    # 如果没有收到token报错

    if not receive_token:
        return '无token'
    #	新建一个isdangerous对象，将密钥传入

    ts_obj = ts(settings.SECRET_KEY)

    # 用带密钥的isdangerous对象解码传入token，注意两次密钥都是相同的

    data = ts_obj.loads(receive_token)

    # 获取token解码后的信息
    username = data['username']
    email = data['email']
    list_ = [username, email]
    return list_

def User_login(username, password):

    if_name_right = User.objects.filter(username=username).first()
    if_password_right = User.objects.filter(password=password).first()
    if_isactive = User.objects.filter(username=username, password=password).values('active_email').first()['active_email']

    if not if_name_right:
        return '用户名错误'
    if not if_password_right:
        return '密码错误'
    if not if_isactive:
        return '邮箱未激活'
    return '登陆成功'



