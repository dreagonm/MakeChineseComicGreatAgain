from rest_framework.views import APIView
# Create your views here.
from Bullet.serializers_ import BulletSerializer
from rest_framework.response import Response
from Bullet.models import WordBullet
from Bullet import func


class BulletMessage(APIView):
    authentication_classes = []

    def post(self, request):
        # 保存弹幕信息
        serializer = BulletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({
                'success': 'false',
            })

        return Response({
            'success': 'true',
        })

    def get(self, request):
        # 获取弹幕信息

        objs = WordBullet.objects.all()
        bullet_dic = func.bullet_get(objs)
        return Response(bullet_dic)

