from Login.models import User
from rest_framework import serializers
import re
from itsdangerous import TimedJSONWebSignatureSerializer as ts
from django.conf import settings
from django.core.mail import send_mail


class UserSerializers(serializers.ModelSerializer):
    def validate(self, attr):
        username = attr.get('username')
        password = attr.get('password')
        email = attr.get('email')
        # 验证邮箱
        if not re.match(r'.*?@.*?\\..*?', email):
            raise serializers.ValidationError('邮箱格式错误')
        if_email = User.objects.filter(Email=email).first()
        if if_email:
            raise serializers.ValidationError('邮箱已注册')
        # 验证用户名是否重复

        if_name = User.objects.filter(Username=username).first()
        if if_name:
            raise serializers.ValidationError('用户名重复')

        # 验证密码安全性（至少8位数并且包含数字字母）
        if len(password) < 8:
            raise serializers.ValidationError('密码少于8位数')
        elif password.isdigit() or password.isalpha():
            raise serializers.ValidationError('密码至少为数字与字母的结合')

    def update(self, instance, validated_data): # TODO：debug邮箱认证
        # instance是从数据库查询出的对象
        instance.email = validated_data['email']
        instance.id = validated_data['id']
        instance.username = validated_data['username']
        # 这里更新一次email字段数据
        instance.save()
        # 创建一个isdangerous的对象，传入我们设置中的密钥
        idsfy = ts(settings.SECRET_KEY)
        # print(idsfy)
        data = {
            'user_id': instance.id,
            'username': instance.username,
            'email': instance.email,
        }

        # 生成isdangerous token
        token = idsfy.dumps(data).decode()
        # 拼接路径
        url = 'http://127.0.0.1:8000/email/vary/?token=' + token
        # 拼接邮件内容
        url_str = '<a href=' + url + '>click to verify ur email</a>'
        # print(instance)
        email_url = validated_data['email']
        # print(email_url)
        # 发送验证邮件
        send_mail(subject='hermit email active', message=url_str, from_email=settings.EMAIL_FROM,
                  recipient_list=[email_url], html_message=url_str)

        return instance

    class Meta:
        model = User
        fields = '__all__'
