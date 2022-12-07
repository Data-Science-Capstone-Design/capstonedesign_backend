from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,
                    id,
                    username,
                    birth,
                    gender,
                    email,
                    phone_num,
                    job,
                    password,
                    address
                    ): # user 생성 함수 
        user=self.model(
            id = id,
            username=username,
            birth=birth,
            gender=gender,
            email=email,
            phone_num=phone_num,
            job=job,
            address=address
        ) 
        user.set_password(password)

        user.save(using=self._db) # settings에 db중 기본 db 사용한다는 의미
        return user
    
    def create_superuser(self,id,password): # superuser 생성 함수 
        user = User.objects.create(
            id = id
        )
        user.set_password(password)

        user.is_superuser=True
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user
# is_active(일반사용자)랑 is_admin은 장고 유저 모델의 필수필드라 정의
# is_staff(사이트관리스탭->이 값이 true여야 관리자페이지 로그인 가능)
# is_superuser는 관리자 페이지의 내용을 제한없이 봄

# PermissionMixin: admin계정 로그인시 사용자 권한 요구하는데 그때 해결 
# AbstractBaseUser는 기존필드 만족안하고 완전히 새로운 모델 생성할때 
class User(AbstractBaseUser,PermissionsMixin):
    id = models.CharField(primary_key=True, unique=True, max_length=100)
    username=models.CharField(max_length=100, null=True,blank=True)
    birth=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=30, null=True,blank=True)
    email=models.EmailField(max_length=200,null=True,blank=True)
    phone_num=models.CharField(max_length=100, null=True,blank=True)
    job=models.CharField(max_length=30, null=True,blank=True)
    cash=models.IntegerField(default=0)
    password=models.CharField(max_length=200,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)


    is_active = models.BooleanField(default=True)
    is_superuser= models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'id' #고유식별자

class Payment_details(models.Model): #결제 내역
    address=models.CharField(max_length=200,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    balance=models.IntegerField(null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    seller=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sellers')
    time=models.DateTimeField(null=True,blank=True)

# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,db_column='user')
#     cash = models.IntegerField(default=0,blank=True,null=True)
#     job=models.CharField( max_length=50,null=True,blank=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
