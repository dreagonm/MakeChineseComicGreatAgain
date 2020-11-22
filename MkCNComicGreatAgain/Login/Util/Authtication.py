from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
from Login.models import User


class Auth(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')

        ts_obj = ts(settings.SECRET_KEY)
        try:
            data = ts_obj.loads(token)

            # 获取token解码后的信息
            username = data['username']
            email = data['email']

            user_object = User.objects.filter(username=username, email=email).first()
            if user_object:
                return username, token
        except:
            raise exceptions.AuthenticationFailed('用户认证失败')

    def authenticate_header(self, request):
        pass