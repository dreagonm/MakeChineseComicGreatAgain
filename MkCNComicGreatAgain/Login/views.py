from Login.models import User
from Login.Util.serializers import UserSerializers
from Login.Util import func
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class UserRegister(APIView):
    authentication_classes = []

    def post(self,request, *args, **kwargs):
        # post的data 中包含属性为 username, password, email
        email = request.data.get('email')
        username = request.data.get('username')
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 发送激活邮件
            func.Email_send(id, username, email, 1)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        # 输入 username 和 password
        # 此处是登陆界面
        # 账号密码验证
        username = request.data.get('username')
        password = request.data.get('password')

        text = func.User_login(username, password)
        if text == '登陆成功':
        # token获取
            user = User.objects.get(username=username, password=password, )
            token = func.Create_Token(user.id, user.username, user.email)
            return HttpResponse(token)
        else:
            return HttpResponse(text)

    def put(self, request, *args, **kwargs):
        # 此处找回密码
        username = request.data.get('username')
        email = request.data.get('email')
        if username != '':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response('无此用户', status=status.HTTP_404_NOT_FOUND)
        elif email != '':
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response('无此用户', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('不能为空')
        if user.active_email == 0:
            return Response('邮箱未激活')
        func.Email_send(user.id, user.name, user.email, 2)


class UserDetail(APIView):

    def get(self, request, name):
        assert request.user == name
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializers(user)
        return Response(serializer.data)


class EmailVaryView(APIView):

    def get(self,request):

        if request.query_params.get('type') == None :

            # 得到url中的token信息
            receive_token = request.query_params.get('token')
            # 验证token, 并从token中获取用户信息
            user_list = func.Email_Vary(receive_token)

            user_obj=User.objects.get(id=user_list[0],username=user_list[1],email=user_list[2])
            user_obj.active_email = True
            user_obj.save()
            return Response('邮箱激活成功')
        else:
            # 此时转到put 即重置密码
            return Response('该用户已激活')

    def put(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user_list = func.Create_Token(token)
        user_obj = User.objects.get(id=user_list[0], username=user_list[1], email=user_list[2])
        password = request.data.get('password')
        user_obj.password = password
        return Response('密码重置成功')




