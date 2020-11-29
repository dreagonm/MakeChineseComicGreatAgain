from django.db import models

bullet_type = (
    (0, u'common'),
    (1, u'advanced')
)


class WordBullet(models.Model):

    bullet = models.CharField(max_length=128)
    typeface = models.CharField(max_length=64, default='宋体')
    color = models.CharField(max_length=16, default='#000000')
    type = models.IntegerField(choices=bullet_type, default=0)
    size = models.CharField(max_length=2, default=16)

    class Meta:
        db_table = 'wordbullet_table'
        verbose_name = u'弹幕信息'
        verbose_name_plural = u'弹幕信息'




