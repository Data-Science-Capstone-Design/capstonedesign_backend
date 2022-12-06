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
from django.utils import timezone

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
    
    userserializer=UserSerializer(request.user,data=body)

    if userserializer.is_valid(raise_exception=True):
        token=userserializer.save()
    return Response(token,status=status.HTTP_201_CREATED)
    

#------------- 바우처 등록 --------------
@api_view(['PUT'])
def voucher_registration(request):
    body=json.loads(request.body)
    result={}
    voucher=Voucher.objects.filter(pin_num=body['pin_num'])
    if voucher.exists():
        voucher=voucher.first()
        if voucher.use is None:
            request.user.cash+=voucher.price
            request.user.save()
            # voucher.price=0
            voucher.use=timezone.now()
            voucher.save()
            result['voucher']=voucher.price
            result['user_cash']=request.user.cash
        else:
            logging.info("이미 사용한 쿠폰")
            return Response(status=status.HTTP_403_FORBIDDEN)
            
    return Response(result,status=status.HTTP_201_CREATED)

#-------------  내 잔액 --------------
@api_view(['GET'])
def info_and_balance(request):
    return Response({"balance":request.user.cash,"user":request.user.id},status=status.HTTP_200_OK)
# #-------- 결제자 정보 확인 -------
# @api_view(['GET'])
# def check_who(request,id):
#     who=User.objects.get(id=id)
#     return Response({"balance":request.user.cash,"user":request.user.id},status=status.HTTP_200_OK)
