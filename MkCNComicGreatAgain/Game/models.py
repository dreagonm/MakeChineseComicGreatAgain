from django.db import models

# Create your models here.

class Character(models.Model):
    # 描述
    description = models.TextField()
    name = models.CharField(max_length=100) 
    isAnswer=models.BooleanField(default=False)
