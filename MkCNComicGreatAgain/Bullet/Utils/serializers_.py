from rest_framework import serializers
from Bullet import models


class BulletSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WordBullet
        fields = '__all__'
