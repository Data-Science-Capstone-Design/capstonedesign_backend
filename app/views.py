from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from django.contrib.auth.models import User
import json
from web.models import *
from django.contrib.auth import authenticate,logout,login

# Create your views here.

def test(request):
    return render(request,'test.html')

@api_view(['POST'])
def signup(request):
    body=json.loads(request.body)
    print(body)
    user=User.objects.create_user(
        username=body['username'],
        password=body['password']
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request): #로그인 수정 필요
    body=json.loads(request.body)
    
    user = authenticate(username=body['username'],password=body['password'])
    if user is not None:
        login(request,user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def coupon_registration(request):
    body=json.loads(request.body)

    pin=Pin.objects.filter(pin_num=body['pin_num'])
    print(pin)
    if pin.exists():
        print('hi')
        request.user.profile.cash+=pin.first().price
        request.user.profile.save()
        pin.price=0
        pin.save()
    
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_my_cash(request):
    return Response({'cash':request.user.profile.cash},status=status.HTTP_200_OK)
