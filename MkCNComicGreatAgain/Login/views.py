from Login.models import User
from Login.serializers import UserSerializers
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
import json
from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


class UserRegister(APIView):
    def post(self,request, *args, **kwargs):
        # post的data 中包含属性为 username, password, email
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        serializer = UserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 以下是邮箱发送

            id = User.objects.filter(username=username).values('id').first()
            # 创建一个isdangerous的对象，传入我们设置中的密钥
            idsfy = ts(settings.SECRET_KEY)
            print(idsfy)
            data = {
                'user_id': id,
                'username': username,
                'email': email,
            }
            # 生成isdangerous token
            token = idsfy.dumps(data).decode()
            # 拼接路径
            print(token)
            url = 'http://127.0.0.1:8000/Login/email/vary/?token=' + token
            # 拼接邮件内容
            url_str = '<a href=' + url + '>click to verify ur email</a>'
            # print(instance)
            email_url = email
            # print(email_url)
            # 发送验证邮件
            send_mail(subject='hermit email active', message=url_str, from_email=settings.EMAIL_FROM,
                      recipient_list=[email_url], html_message=url_str)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        # 输入 username 和 password

        username = request.data.get('username')
        password = request.data.get('password')
        if_name_right = User.objects.filter(username=username).first()

        if_password_right = User.objects.filter(password=password).first()
        if_isactive = User.objects.filter(username=username,password=password).values('active_email').first()
        print(if_name_right)
        if not if_name_right:
            return HttpResponse('用户名错误')
        if not if_password_right:
            return HttpResponse('密码错误')
        if if_isactive:
            return HttpResponse('邮箱未激活')
        return HttpResponse('登陆成功')


class UserDetail(APIView):

    def get_object(self, name):
        try:
            return User.objects.get(UserName=name)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, name):
        user = self.get_object(name)
        serializer = UserSerializers(user)
        return Response(serializer.data)


class EmailVaryView(APIView):

    def get(self,request):
        # 得到url中的token信息
        receive_token = request.query_params.get('token')
        print('#############email#########')
        print(receive_token)
        # 如果没有收到token报错
        if not receive_token:
            return Response({'err_msg:lack token'}, status=401)
        #	新建一个isdangerous对象，将密钥传入
        ts_obj = ts(settings.SECRET_KEY)
        # 用带密钥的isdangerous对象解码传入token，注意两次密钥都是相同的
        data=ts_obj.loads(receive_token)
        print(data)
        # 获取token解码后的信息
        user_id=data['user_id']['id']

        username= data['username']
        email = data['email']
        # 用信息获取用户对象
        user_obj=User.objects.get(id=user_id,username=username,email=email)
        print(user_obj)
        # 将用户对象中的字段信息修改并保存
        user_obj.active_email = True
        user_obj.save()
        return Response('Okay')