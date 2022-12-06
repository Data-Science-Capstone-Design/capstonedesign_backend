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


User=get_user_model()

def main(request):
    data_list=[]
    excel_inst=Excel_data.objects.filter(main=True)
    if excel_inst.exists():
        excel_inst=excel_inst.first()
        data_list=excel_inst
    return render(request, 'html/index.html',{'data_list':data_list})

def excel_save(request):
    excel=request.FILES.get('excel_file')
    print(request.POST)
    print(excel)
    filename,fileExtension=os.path.splitext(str(excel))
    print(filename)
    print(fileExtension)
    if fileExtension == '.xlsx':
        group=timezone.now().strftime('%Y/%m/%d - %H:%M:%S')
        df=pd.read_excel(excel)
        for i in df:
            print(i)
            Excel_data.objects.create(
                group=group,
                username=i['이름'],
                birth=i['생년월일'],
                address=i['주소'],
                phone_num=i['전화번호']
            )
        print(df)
    else:
        messages.warning(request, "확장자가 xlsx가 아닙니다")

    return redirect('web:main')

#------------- 쿠폰 생성페이지 --------------
def make_voucher_page(request):
    return render(request,'make_voucher.html')

#------------- 쿠폰 생성 --------------
def make_vouchers(request): # 겹치는거 기능 추가해야함
    
    pin_num = request.POST["pin_num"]
    price = request.POST["price"]

    if Voucher.objects.exists(pin_num=pin_num):
        messages.warning(request, "이미 존재하는 바우처 입니다")
    else:
        Voucher.objects.create(
            pin_num=pin_num,
            price=price
        )

    return redirect('web:main')

# #------------- 메인 페이지 --------------
# def main(request):
#     return render(request,'main.html')

#------------- 쿠폰 열람 페이지 --------------
def show_vouchers(request):
    vouchers=Voucher.objects.all()
    return render(request,'voucher_list.html',{"vouchers":vouchers})


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
def about(request):
    return render(request, 'html/about.html')

def view(request):
    return render(request, 'html/classes.html')


def set_main_page_excel(request):
    excel_main=Excel_data.objects.filter(main=True)
    excel_inst=Excel_data.objects.get(group=request.POST['main_page_excel'])

    if excel_main.exists():
        excel_main=excel_main.first()
        if excel_main!=excel_inst:
            excel_main.main=False
            excel_inst.main=True
            excel_main.save()
            excel_inst.save()
    return redirect("web:main")
