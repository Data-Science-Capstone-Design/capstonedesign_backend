#from msilib.schema import Billboard

from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .forms import UploadFileForm
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth import get_user_model
from django.contrib import messages
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
import pandas as pd
import os
# Imaginary function to handle an uploaded file.
from .forms import handle_uploaded_file
# 엑셀을 생성 및 행 추가 (여기서는 행 단위 추가만 함 열만 추가하는건 검색 바람 )
# from openpyxl import Workbook # 엑셀을 만드는 api (엑셀 미설치 시에도 동작)
# from io import BytesIO # 엑셀 파일을 전송 할 수 있도록 바이트 배열로 변환
User=get_user_model()


def upload_file(request):
    if request.method == 'POST':
       
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        print(request.POST)
        print(form)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('webtest')
    else:
        form = UploadFileForm()

    return render(request, 'webtest.html', {'form': form})


def excel_save(request):
    excel=request.FILES.get('excel_file')
    print(request.POST)
    print(excel)
    filename,fileExtension=os.path.splitext(str(excel))
    print(filename)
    print(fileExtension)
    if fileExtension == '.xlsx':
        df=pd.read_excel(excel)
        
        print(df)
    else:
        messages.warning(request, "확장자가 xlsx가 아닙니다")

    return redirect('web:main')

#------------- 쿠폰 생성페이지 --------------
def make_coupon_page(request):
    return render(request,'make_coupon.html')

#------------- 쿠폰 생성 --------------
def make_coupon(request): # 겹치는거 기능 추가해야함
    
    coupon_num = request.POST["coupon_num"]
    price = request.POST["price"]

    Coupon.objects.create(
        coupon_num=coupon_num,
        price=price
    )

    return redirect('web:main')

#------------- 메인 페이지 --------------
def main(request):
    return render(request,'main.html')

#------------- 쿠폰 열람 페이지 --------------
def show_coupons(request):
    coupons=Coupon.objects.all()
    return render(request,'coupon_list.html',{"coupons":coupons})


#------------- 회원가입 페이지 --------------
def signuppage(request):
    return render(request,'accounts/signup.html')

#------------- 회원가입 --------------
def signup(request):
    user=User.objects.create_user(
        id=request.POST['id'],
        password=request.POST['password'],
    )
    user.profile.job=request.POST['job']
    user.profile.save()
    login(request,user)
    return redirect('web:main')

#------------- 로그인 페이지 --------------
def loginpage(request):
    return render(request,'accounts/login.html')

def login_view(request):
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

# # ----------- 메일 전송 --------------
# def mail_send(reqeust):
#     mail_subject='지원금 수령자로 선정되셨습니다' #메일 제목
#     message=render_to_string('smtp_email.html')