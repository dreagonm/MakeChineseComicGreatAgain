from Game.models import Character
from Game.serializers import CharacterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json

# Create your views here.

class Guess(APIView):
    # 新建角色
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        dic = request.data
        # print(type(dic))  
        dic_str=json.dumps(dic)
        name = dic['name']
        try:
            Character.objects.get(name=name)
        except Character.DoesNotExist:
            data = {'description':dic_str,'name': name}
            serializer = CharacterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response({'success':'false'})
        else:
            return Response({'success':'false'})

    # 获取角色信息
    def get(self,request,*args,**kwargs):
        if Character.objects.count()==0:
            return Response('NoCharacter')
        numCharacter = random.randint(0,Character.objects.count()-1)
        fileCharacter = Character.objects.all()[numCharacter]
        fileCharacter.isAnswer=True
        fileCharacter.save()
        dic = json.loads(fileCharacter.description)
        name = fileCharacter.name
        dic['name']=name
        return Response(data=dic)
        

    # 提交答案
    def put(self,request,*args,**kwargs):
        ans=request.data.get('name')
        try:
            fileCharacter = Character.objects.get(name=ans)
        except Character.DoesNotExist:
            return Response({'result':'wrong'})
        if fileCharacter.isAnswer:
            fileCharacter.isAnswer=False
            fileCharacter.save()
            return Response({'result':'right'})
        else:
            return Response({'result':'wrong'})

    def delete(self,request,*args,**kwargs):
        name=request.data.get('name')
        fileCharacter = Character.objects.filter(name=name)
        for character in fileCharacter:
            character.delete()
        return Response({'result':'success'})