from django.shortcuts import render,redirect
# from .forms import UploadFileForm
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth import get_user_model
from django.contrib import messages
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
import pandas as pd
import os
from django.utils import timezone
from django.db.models import Q,F,Value,Func,Count,Sum,CharField
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from app.models import Payment_details
from django.conf import settings
import requests
import time
import sys
import hashlib
import hmac
import base64

User=get_user_model()

def main(request):
   
    return render(request, 'html/index.html')

def excel_save(request):
    excel=request.FILES.get('excel_file')
    print(request.POST)
    print(excel)
    filename,fileExtension=os.path.splitext(str(excel))
    print(filename)
    print(fileExtension)
    if fileExtension == '.xlsx':
        group=str(timezone.now().strftime('%Y/%m/%d - %H:%M:%S'))
        df=pd.read_excel(excel)
        for j,i in df.iterrows():
            # print(group)
            # print(type(group))
            # print(i['생년월일'])
            Excel_data.objects.create(
                group=group,
                username=i['이름'],
                birth=i['생년월일'],
                address=i['주소'],
                phone_num=i['전화번호'],
                writer=request.user
            )
        print(df)
    else:
        messages.warning(request, "확장자가 xlsx가 아닙니다")

    return redirect('web:about')

#------------- 쿠폰 생성페이지 --------------
def make_voucher_page(request):
    return render(request,'make_voucher.html')

#------------- 쿠폰 생성 --------------
def make_vouchers(request): # 겹치는거 기능 추가해야함
    
    pin_num = request.POST["voucher_num"]
    price = request.POST["price"]
    
    if Voucher.objects.filter(pin_num=pin_num).exists():
        messages.warning(request, "이미 존재하는 바우처 입니다")
    else:
        Voucher.objects.create(
            pin_num=pin_num,
            price=price,
            issuer=request.user
        )

    return redirect('web:close')


#------------- 쿠폰 상태 페이지 --------------
def show_vouchers(request):
    vouchers=Voucher.objects.filter(issuer=request.user)
    return render(request,'html/voucher.html',{"vouchers":vouchers})
#------------- 결제 내역 페이지 --------------
def payment_page(request):

    payments=Payment_details.objects.filter(user=request.POST['user'])
    return render(request,'html/voucher.html',{"payments":payments})


#------------- 회원가입 페이지 --------------
def signuppage(request):
    return render(request,'accounts/signup.html')

#------------- 회원가입 --------------
def signup(request):
    user=User.objects.create_user(
        id=request.POST['id'],
        password=request.POST['password'],
    )
    user.job=request.POST['job']
    user.save()
    login(request,user)
    return redirect('web:main')

#------------- 로그인 페이지 --------------
def loginpage(request):
    return render(request,'accounts/login.html')

def login_view(request):
    print()
    user=authenticate(id=request.POST['id'],password=request.POST['password'])
    if user is not None:
        login(request,user)
        return redirect('web:main')
    else:
        messages.warning(request, "비밀번호가 틀렸거나 회원이 아닙니다.")
        return redirect('web:main')

#------------- 로그아웃 --------------
def logout_view(request):
    logout(request)
    return redirect('web:main')

#------------- 엑셀 다운로드 --------------
def download_excel(request):
  
    file_path = os.path.abspath("web/static/excel/")
    file_name = os.path.basename("web/static/excel/default.xlsx")
    print(file_path)
    print(file_name)
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="default.xlsx"'

    return response

# # ----------- 메일 전송 --------------
# def mail_send(reqeust):
#     mail_subject='지원금 수령자로 선정되셨습니다' #메일 제목
#     message=render_to_string('smtp_email.html')
def about(request):
    excels=Excel_data.objects.filter(writer=request.user)
    excel_group=excels.values('group').annotate(ct=Count('group'))

    main_group=None
    main_excel_data=None
    mx=Main_excel.objects.filter(user=request.user)
    if mx.exists():
        mx=mx.first()
        main_group=mx.group
        main_excel_data=excels.filter(group=mx.group)

    context={
        "excel_group":excel_group,
        "main_excel_data":main_excel_data,
        "main_group":main_group
    }

    return render(request, 'html/about.html',context)



def set_main_page_excel(request):
    main=Main_excel.objects.filter(user=request.user)
    print(request.POST['main_page_excel'])
    if main.exists():
        main=main.first()
        main.group=request.POST['main_page_excel']
        main.save()
    else:
        main=Main_excel.objects.create(
            user=request.user,
            group=request.POST['main_page_excel']
        )
    
    return redirect("web:about")

def register_product(request):
    Product.objects.create(
        name=request.POST['name'],
        price=request.POST['price'],
        admin=request.user,
        possible=request.POST['possible'],
    )
    return redirect("web:main")

def send_sms_page(request,phone_num):
    return render(request,"html/send_sms_page.html",{"phone_num":phone_num})

def send_sms(request):
    pin=request.POST['pin_num']
    print(pin)
    print(request.POST['phone_num'])
    sms(request.POST['phone_num'],pin)
    vou=Voucher.objects.get(pin_num=pin)
    vou.issue=timezone.now()
    vou.save()
    return redirect("web:close")
def close(request):
    return render(request,'close.html')

def	make_signature(access,secret):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    access_key = "{}".format(access)
    secret_key = "{}".format(secret)
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    uri = "/photos/puppy.jpg?query1=&query2"
    message = method + " " + uri + "\n" + timestamp + "\n"+ access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey
def make_signature(access,secret):
    secret_key = bytes(secret, 'UTF-8')
    access = bytes(access, 'UTF-8')
    string_hmac = hmac.new(secret_key, access, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64

def sms(phone_num,pin_num):
    phone_num=phone_num.replace("-","")
    SMS_ACCESS = getattr(settings, 'SMS_ACCESS', None)
    SMS_SECRET = getattr(settings, 'SMS_SECRET', None)
    SMS_SERVICE_ID = getattr(settings, 'SMS_SERVICE_ID', None)
    SEND_PHONE = getattr(settings, 'SEND_PHONE', None)

    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': str(int(time.time() * 1000)),
        'x-ncp-iam-access-key': f'{SMS_ACCESS}',
        'x-ncp-apigw-signature-v2':make_signature(SMS_ACCESS,SMS_SECRET)
    }
    print(headers)
    data={
        'type':'SMS',
        'contentType':'COMM',
        'countryCode':'82',
        'from':f'{SEND_PHONE}',
        'content':"[강남한끼]",
        'messages':[
            {
                "to":f'{phone_num}',
                'content':"바우처 번호 : {}\n 해당 바우처 번호를 등록하고 강남한끼를 통해 편의점에서 생필품을 구입해보아요!".format(pin_num),
            }
                
            ],
    }
    print(data)
    res=requests.post('https://sens.apigw.ntruss.com/sms/v2/services/{}/messages'.format(SMS_SERVICE_ID), headers=headers, json=data)
    print(res.status_code)