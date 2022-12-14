from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model
User=get_user_model()

# class Document(models.Model):
#     uploadedFile = models.FileField('첨부파일',upload_to = "files/")


class Voucher(models.Model): #바우처 정보
    pin_num=models.CharField(unique=True, max_length=100,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    use=models.DateTimeField(null=True,blank=True)
    issue=models.DateTimeField(null=True,blank=True)
    issuer=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 

    # use=models.BooleanField(default=False) #사용여부
    # issue=models.BooleanField(default=False) #발급여부

class Product(models.Model): # 더미데이터용
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    admin=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    possible=models.BooleanField(default=True)

class Excel_data(models.Model):
    group=models.CharField(max_length=100,null=True,blank=True) #그룹

    username=models.CharField(max_length=100, null=True,blank=True)
    birth=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    phone_num=models.CharField(max_length=100, null=True,blank=True) #엑셀
    
    send=models.BooleanField(default=False) # 전송여부
    app_user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="app_user") # 매칭
    writer=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="writer") # 매칭

class Main_excel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,db_column='user')
    group=models.CharField(max_length=100,null=True,blank=True) #그룹

# class Candidate(models.Model):
#     name = models.CharField(max_length=10)
#     introduction = models.TextField()
#     area = models.CharField(max_length=15)
#     #party_number = models.IntegerField(default=0)
#     def __str__(self):
#         return 'name : {},introduction : {},area : {}'.format(self.name ,self.introduction, self.area)
