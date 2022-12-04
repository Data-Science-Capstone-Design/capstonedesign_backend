from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework import status 
import json
from web.models import *
from django.contrib.auth import authenticate,logout,login
from .serializers import *
import logging as logger
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
import logging
# Create your views here.

#------------- 회원가입 --------------
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    body=json.loads(request.body)

    userserializer=UserSerializer(data=body)

    if userserializer.is_valid(raise_exception=True):
        token=userserializer.save()
    return Response(token,status=status.HTTP_201_CREATED)

#------------- 프로필 업데이트 --------------
@api_view(['PUT'])
def update_profile(request):
    body=json.loads(request.body)
    
    profileserializer=ProfileSerializer(request.user.profile,data=body)

    if profileserializer.is_valid(raise_exception=True):
        profile=profileserializer.save()
    return Response(status=status.HTTP_201_CREATED)
    

#------------- 쿠폰 등록 --------------
@api_view(['PUT'])
def coupon_registration(request):
    body=json.loads(request.body)
    result={}
    coupon=Coupon.objects.filter(coupon_num=body['coupon_num'])
    if coupon.exists():
        coupon=coupon.first()
        if coupon.use==False:
            request.user.profile.cash+=coupon.price
            request.user.profile.save()
            coupon.price=0
            coupon.use=True
            coupon.save()
            result['coupon']=coupon.price
            result['user_cash']=request.user.profile.cash
        else:
            logging.info("이미 사용한 쿠폰")
            return Response(status=status.HTTP_403_FORBIDDEN)
            
    return Response(result,status=status.HTTP_201_CREATED)

#-------------  내 잔액 --------------
@api_view(['GET'])
def get_my_cash(request):
    cash_info=UserCashSerializer(request.user.profile).data
    return Response(cash_info,status=status.HTTP_200_OK)
