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
        # print(request.FILES)
        print(request.FILES.get('file'))
        # print(request.POST)
        print(form)
        if form.is_valid():
            print('form')
          
            handle_uploaded_file(request.FILES)
            return redirect('web:about')

    else:
        form = UploadFileForm()

    # return render(request, 'templatemo_555_upright/.html', {'form': form})
    return redirect('web:about')


def main(request):
    data_list=[]
    return render(request, 'html/index.html',{'data_list':data_list})

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
def about(request):
    return render(request, 'html/about.html')

def view(request):
    return render(request, 'html/classes.html')

# def csvTomodel(request):
#     path='/Users/songryu/Desktop/capstonedesign_backend/web/media/files/data.xlsx'
#     file=open(path)
#     reader=csv.reader(file)
#     print('----',reader)
#     list=[]
#     for row in reader:
#         list.append(seops(a=row[0],
#                           b=row[1],
#                           c=row[2]))
#     seops.objects.bulk_create(list)                    
#     return HttpResponse('create model --')


# def main_view(request):
#     with open('web/media/files/data.xlsx','r') as f:
#         dr = csv.DictReader(f)
#         s = pd.DataFrame(dr)
#     ss = []
#     for i in range(len(s)):
#         st = (s['이름'][i], s['나이'][i], s['주소'][i])
#         ss.append(st)
#     for i in range(len(s)):
#         Candidate.objects.create(name=ss[i][0], code=ss[i][1], ipo_date=ss[i][2])
#         context={'df':s.to_html(justify='center')}
#         return render(request,'classes.html',context)
