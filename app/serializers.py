from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
    def create(self, validated_data):
        user=User.objects.create_user(
            id=validated_data['id'],
            password=validated_data['password']
            )
        
        refresh=RefreshToken.for_user(user)
        return {"refresh":str(refresh),"access":str(refresh.access_token)} #회원가입시 바로 access토큰 refresh 토큰 생성후 리턴

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class UserCashSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['cash']
