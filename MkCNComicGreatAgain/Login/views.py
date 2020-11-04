from Login.models import User
from Login.serializers import UserSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserList(APIView):
    def post(self,request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self,name):
        try:
            return User.objects.get(UserName=name)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,name):
        user = self.get_object(name)
        serializer=UserSerializers(user)
        return Response(serializer.data)
    

