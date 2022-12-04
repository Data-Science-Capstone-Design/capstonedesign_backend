#from msilib.schema import Billboard
from django.shortcuts import render,redirect
from .models import Document
from .forms import PostForm,UploadFileForm,handle_uploaded_file
from django.http import HttpResponse,HttpResponseRedirect 
from .models import Candidate
import csv
import pandas as pd

"""
# Create your views here.
def test(request):
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

def about(request):
    return render(request, 'html/about.html')

def view(request):
    return render(request, 'html/classes.html')

def csvTomodel(request):
    path='/Users/songryu/Desktop/capstonedesign_backend/web/media/files/data.xlsx'
    file=open(path)
    reader=csv.reader(file)
    print('----',reader)
    list=[]
    for row in reader:
        list.append(seops(a=row[0],
                          b=row[1],
                          c=row[2]))
    seops.objects.bulk_create(list)                    
    return HttpResponse('create model --')


def main_view(request):
    with open('web/media/files/data.xlsx','r') as f:
        dr = csv.DictReader(f)
        s = pd.DataFrame(dr)
    ss = []
    for i in range(len(s)):
        st = (s['이름'][i], s['나이'][i], s['주소'][i])
        ss.append(st)
    for i in range(len(s)):
        Candidate.objects.create(name=ss[i][0], code=ss[i][1], ipo_date=ss[i][2])
        context={'df':s.to_html(justify='center')}
        return render(request,'classes.html',context)
