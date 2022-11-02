from django.db import models
from django.db.models import Model
# Create your models here.

class Document(models.Model):
    uploadedFile = models.FileField('첨부파일',upload_to = "files/")


class Pin(models.Model):
    pin_num=models.CharField(unique=True, max_length=100,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
