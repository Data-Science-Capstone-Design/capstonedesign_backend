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
from django.contrib.auth import get_user_model
User=get_user_model()

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
    

#------------- 사용자 바우처 등록 --------------
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

#-------- 물품 가격 조회 --------
@api_view(['GET'])
def price_inquiry(request,id):
    product=Product.objects.get(id=id)
    result=ProductInfoSerializer(product).data
    return Response(result,status=status.HTTP_200_OK)
 
#-------- 결제자 입장 : 결제 -------
# 구매 불가능 물품 포함한지 체크하고, 잔액과 총 액 비교해서 결제 가능하면 결제 후 결제 내역 DB에 기록 남기기 까지
@api_view(['PUT'])
def payment(request):
    body=json.loads(request.body) # product_list:[], user_id:id
    flag=True
    price_sum=0
    for pd_id in body['product_list']:
        pd=Product.objects.get(id=pd_id)
        price_sum+=pd.price
        if pd.possible==False:
            flag=False
            break
    if flag==False:
        return Response({"reason":"구매 불가능 물품 포함"},status=status.HTTP_403_FORBIDDEN)
    else:
        user=User.objects.get(id=body['user_id'])
        if user.cash>=price_sum:
            user.cash-=price_sum
            user.save()

            payment_history=Payment_details.objects.create(
                address=request.user.address,
                price=price_sum,
                balance=user.cash,
                user=user,
                seller=request.user
            )

            return Response({"remain_cash":user.cash},status=status.HTTP_201_CREATED)
        else:
            return Response({"reason":"잔액 부족"},status=status.HTTP_403_FORBIDDEN)
