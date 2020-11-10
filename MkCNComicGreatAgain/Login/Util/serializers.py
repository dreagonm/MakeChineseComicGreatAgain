from Login.models import User
from rest_framework import serializers
import re


class UserSerializers(serializers.ModelSerializer):
    def validate(self, attr):
        username = attr.get('username')
        password = attr.get('password')
        email = attr.get('email')
        # 验证邮箱
        if not re.match(r".*?@.*?\..*?", email):

            raise serializers.ValidationError('邮箱格式错误')
        if_email = User.objects.filter(email=email).first()
        if if_email:
            raise serializers.ValidationError('邮箱已注册')
        # 验证用户名是否重复

        if_name = User.objects.filter(username=username).first()
        if if_name:
            raise serializers.ValidationError('用户名重复')

        # 验证密码安全性（至少8位数并且包含数字字母）
        if len(password) < 8:
            raise serializers.ValidationError('密码少于8位数')
        elif password.isdigit() or password.isalpha():
            raise serializers.ValidationError('密码至少为数字与字母的结合')
        return attr

    class Meta:
        model = User
        fields = '__all__'


