from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth.hashers import make_password
from web.models import Product
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
    def create(self, validated_data):
        # print(validated_data)
        user=User.objects.create_user(
            id=validated_data.get('id'),
            password=validated_data.get('password'),
            username=validated_data.get('username'),
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            email=validated_data.get('email'),
            phone_num=validated_data.get('phone_num'),
            job=validated_data.get('job'),
            address=validated_data.get('address')
            )
        
        refresh=RefreshToken.for_user(user)
        return {"refresh":str(refresh),"access":str(refresh.access_token)} #회원가입시 바로 access토큰 refresh 토큰 생성후 리턴
    
    def update(self,instance,validated_data):
        if validated_data.get('password',None) is not None:
            instance.password=make_password(validated_data.get('password',instance.password))
       
        instance.username=validated_data.get('username',instance.username)
        instance.birth=validated_data.get('birth',instance.birth)
        instance.gender=validated_data.get('gender',instance.gender)
        instance.email=validated_data.get('email',instance.email)
        instance.phone_num=validated_data.get('phone_num',instance.phone_num)
        instance.job=validated_data.get('job',instance.job)
        instance.address=validated_data.get('address',instance.address)
        instance.save()
        refresh=RefreshToken.for_user(instance)
        return {"refresh":str(refresh),"access":str(refresh.access_token)} #회원가입시 바로 access토큰 refresh 토큰 생성후 리턴

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Profile
#         fields='__all__'

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','price']