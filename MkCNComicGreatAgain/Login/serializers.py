from Login.models import User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    def validate(self,attr): #TODO:checker 逻辑
        pass

    class Meta:
        model = User
        fields = ('UserName','PassWord','Email',)