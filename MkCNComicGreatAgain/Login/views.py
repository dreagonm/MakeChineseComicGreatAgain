from Login.models import User
from Login.Util.serializers import UserSerializers
from Login.Util import func
from rest_framework.views import APIView
from rest_framework.response import Response


class UserRegister(APIView):
    authentication_classes = []

    def post(self,request, *args, **kwargs):
        # post的data 中包含属性为 username, password, email
        # 数据在form-data中
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        return_message = func.Register_Message_Check(email, username, password)

        if return_message != '注册成功，已发送邮件':
            return Response(return_message)
        serializer = UserSerializers(data=request.data)
        serializer.is_valid()
        serializer.save()

        func.Email_send(username, email)

        return Response(return_message)

    def get(self, request, *args, **kwargs):

        # 用户名持续重复检测

        username = request.data.get('username')
        if_right = User.objects.filter(username=username).first()
        if username == '':
            return Response('用户名不能为空')
        if not if_right:
            return Response('用户名重复')
        else:
            return Response('用户名可用')


class UserLogin(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 输入 username 和 password
        # 账号密码验证
        # 数据在form-data中

        username = request.data.get('username')
        password = request.data.get('password')
        text = func.User_login(username, password)

        if text == '登陆成功':
            user = User.objects.get(username=username)
            token = func.Create_Token(username, user.email)
            return Response(token)
        else:
            return Response(text)

    def get(self, request, *args, **kwargs):
        # 数据在form-data中
        token = request.data.get('token')
        print(token)
        user_list = func.From_token(token)

        if user_list == '无token':
            return Response(user_list)

        return Response({'用户名': user_list[0], '邮箱': user_list[1]})


class EmailVaryView(APIView):

    def get(self, request):

        receive_token = request.query_params.get('token')
        print(receive_token)
        user_list = func.From_token(receive_token)
        print(user_list)
        if user_list == '无token':
            return Response(user_list)

        user_obj=User.objects.get(username=user_list[0], email=user_list[1])
        user_obj.active_email = True
        user_obj.save()
        return Response('邮箱激活成功')


class EmailFindView(APIView):

    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        return_message = func.Password_Find_Check(email, username)
        if return_message != '错误':
            func.Email_send(return_message.username, return_message.email, type=2)
            return Response('已发送邮件')
        else:
            return Response(return_message)

    def put(self, request, *args, **kwargs):

        new_password = request.data.get('password')
        receive_token = request.query_params.get('token')
        user_list = func.From_token(receive_token)

        if user_list == '无token':
            return Response(user_list)
        return_message = func.Password_Change(new_password)
        if return_message != '修改密码成功':
            return Response(return_message)
        user_obj = User.objects.get(username=user_list[0], email=user_list[1])
        user_obj.password = new_password
        user_obj.save()
        return Response(return_message)
