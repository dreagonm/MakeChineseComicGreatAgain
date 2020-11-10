from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from Login.models import User


def Create_Token(id, username, email):
    idsfy = ts(settings.SECRET_KEY)
    data = {
        'user_id': id,
        'username': username,
        'email': email,
    }
    # 生成isdangerous token
    token = idsfy.dumps(data).decode()
    return token


def Email_send(id, username, email, type):
    token = Create_Token(id, username, email)
    if type == 1:
        url = 'http://127.0.0.1:8000/Login/email/vary/?token=' + token
    else :
        url = 'http://127.0.0.1:8000/Login/email/find/?token=' + token + '&?type=2'

    # 拼接邮件内容
    url_str = '<a href=' + url + '>click to verify ur email</a>'

    email_url = email
    # 发送验证邮件
    send_mail(subject='hermit email active', message=url_str, from_email=settings.EMAIL_FROM,
              recipient_list=[email_url], html_message=url_str)


def Email_Vary(receive_token):

    # 如果没有收到token报错
    if not receive_token:
        return Response({'err_msg:lack token'}, status=401)
    #	新建一个isdangerous对象，将密钥传入
    ts_obj = ts(settings.SECRET_KEY)
    # 用带密钥的isdangerous对象解码传入token，注意两次密钥都是相同的
    data = ts_obj.loads(receive_token)

    # 获取token解码后的信息
    user_id = data['user_id']
    username = data['username']
    email = data['email']
    list_ = [user_id, username, email]
    return list_

def User_login(username, password):

    if_name_right = User.objects.filter(username=username).first()
    if_password_right = User.objects.filter(password=password).first()
    if_isactive = User.objects.filter(username=username, password=password).values('active_email').first()
    if not if_name_right:
        return '用户名错误'
    if not if_password_right:
        return '密码错误'
    if not if_isactive:
        return '邮箱未激活'
    return '登陆成功'



