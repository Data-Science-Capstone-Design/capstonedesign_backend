from django.db import models
from django.db.models import Model
# Create your models here.

class Document(models.Model):
    uploadedFile = models.FileField('첨부파일',upload_to = "files/")


class Coupon(models.Model):
    coupon_num=models.CharField(unique=True, max_length=100,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    use=models.BooleanField(default=False) #사용여부
    issue=models.BooleanField(default=False) #발급여부
