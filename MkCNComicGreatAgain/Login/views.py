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
            func.Email_send(id, username, email)

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

class UserDetail(APIView):

    def get(self, request, name):
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializers(user)
        return Response(serializer.data)


class EmailVaryView(APIView):

    def get(self,request):
        # 得到url中的token信息
        print(1)
        receive_token = request.query_params.get('token')
        print(2)
        # 验证token, 并从token中获取用户信息
        user_list = func.Email_Vary(receive_token)

        user_obj=User.objects.get(id=user_list[0],username=user_list[1],email=user_list[2])
        user_obj.active_email = True
        user_obj.save()
        return Response('邮箱激活成功')