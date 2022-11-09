#from msilib.schema import Billboard

from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .forms import UploadFileForm
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth import get_user_model
from django.contrib import messages

# Imaginary function to handle an uploaded file.
from .forms import handle_uploaded_file
# 엑셀을 생성 및 행 추가 (여기서는 행 단위 추가만 함 열만 추가하는건 검색 바람 )
# from openpyxl import Workbook # 엑셀을 만드는 api (엑셀 미설치 시에도 동작)
# from io import BytesIO # 엑셀 파일을 전송 할 수 있도록 바이트 배열로 변환
User=get_user_model()
"""
from django.shortcuts import render,redirect
from .models import Document
from .forms import PostForm

# Create your views here.
def test(request):
    
    return render(request,'webtest.html')
    if request.method=='GET': 
        modelform=PostForm()
        return render(request,'webtest.html',{'modelform':modelform}) #postform을 변수에 담아서 webtest.html 을 렌더링
#템플릿 불러오기 
    elif request.method=='POST':
        modelform=PostForm(request.POST) #입력된 내용들 변수에 저장
        if modelform.is_valid(): #form 이 유효하면 
            post=modelform.save(commit=False) #데이터가져옴
            post.files=request.FILES('file')
            post.save() #DB에 저장
            return redirect('webtest.html'+str(post.id)) #URL로 이동

def read(requests,bid):
    post=Document.objects.prefetch_related('post_set').get(id=bid)
    return render(requests,'web/list.html',{'post':post})
"""


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


# wb = Workbook()  # 엑셀 생성
# ws = wb.active	# 엑셀 활성화
# excelfile = BytesIO() #바이트 배열 생성

# ws['A1']= 'company' # 엑셀 a1 열 이름 정하기
# ws['B1']= 'product'
# ws['C1']= 'count'

# for i in text: # text 는 db 에 저장된 내용 전체
#   content=[i.company,i.product_name,i.count]   #리스트 형태로 1 행씩 생성(a1, b1, c1) 에 각각
#   ws.append(content) # 엑셀에 1행을 추가

# wb.close()  #엑셀 닫기
# wb.save(excelfile) # 바이트배열로 저장 (mail 전송 하려면 바이트형태로 변환 되어야 함)

def make_coupon_page(request):
    return render(request,'make_coupon.html')

def make_coupon(request): # 겹치는거 기능 추가해야함
    
    coupon_num = request.POST["coupon_num"]
    price = request.POST["price"]

    Coupon.objects.create(
        coupon_num=coupon_num,
        price=price
    )

    return redirect('web:main')

def main(request):
    return render(request,'main.html')

def show_coupons(request):
    coupons=Coupon.objects.all()
    return render(request,'coupon_list.html',{"coupons":coupons})


def signuppage(request):
    return render(request,'accounts/signup.html')

def signup(request):
    user=User.objects.create_user(
        id=request.POST['id'],
        password=request.POST['password'],
        job=request.POST['job']
    )
    login(request,user)
    return redirect('web:main')

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

def logout_view(request):
    logout(request)
    return redirect('web:main')