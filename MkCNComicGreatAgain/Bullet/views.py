from rest_framework.views import APIView
from Bullet.Utils.serializers_ import BulletSerializer
from rest_framework.response import Response
from Bullet.models import WordBullet
from Bullet.Utils import func


class BulletMessage(APIView):
    authentication_classes = []

    def post(self, request):
        # 保存弹幕信息
        # --------------------
        test_text = request.data.get('bullet')
        # 对文本进行重复性检测
        return_message = func.Re_Check(test_text)
        if return_message:
            serializer = BulletSerializer(data=request.data)
            if serializer.is_valid(True):
                serializer.save()
            else:
                return Response({
                    'success': 'false',
                })

            return Response({
                'success': 'true',
            })
        else:
            return Response({
                'success': 'false'
            })

    def get(self, request):
        # 获取弹幕信息

        objs = WordBullet.objects.all()
        bullet_dic = func.bullet_get(objs)
        return Response(bullet_dic)


class Inform(APIView):  # 举报系统
    authentication_classes = []
    def post(self, request):
        bullet = request.data.get('bullet')
        # 检测敏感词
        # TODO：敏感词检测，
        pass



