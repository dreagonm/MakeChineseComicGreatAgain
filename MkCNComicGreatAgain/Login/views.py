from Login.models import User
from Login.serializers import UserSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
# Create your views here.


class UserList(APIView):
    def post(self,request):
        # post的data 中包含属性为 username, password, email
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
    

class EmailSend(UpdateAPIView):
    serializer_class = UserSerializers

    def get_object(self):
        return self.request.user


class EmailVaryView(APIView):

    def get(self,request):
        # 得到url中的token信息
        receive_token = request.query_params.get('token')
        print('#############email#########')
        print(receive_token)
        # 如果没有收到token报错
        if not receive_token:
            return Response({'err_msg:lack token'},status=401)
        #	新建一个isdangerous对象，将密钥传入
        ts_obj = ts(settings.SECRET_KEY)
        # 用带密钥的isdangerous对象解码传入token，注意两次密钥都是相同的
        data=ts_obj.loads(receive_token)
        print(data)
        # 获取token解码后的信息
        user_id=data['user_id']
        username= data['username']
        email = data['email']
        # 用信息获取用户对象
        user_obj=User.objects.get(id=user_id,username=username,email=email)
        print(user_obj)
        # 将用户对象中的字段信息修改并保存
        user_obj.active_email = True
        user_obj.save()
        return Response('Okay')