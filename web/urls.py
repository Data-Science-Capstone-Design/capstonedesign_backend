
from django.urls import path
from . import views
from .views import *
app_name='web'
urlpatterns = [
    path('webtest',upload_file,name='webtest'),

    path('main',main,name='main'),
    path('make_coupon_page',make_coupon_page,name='make_coupon_page'),
    path('make_coupon',make_coupon,name='make_coupon'),
    #path('postcreate/',views.test,name='test')

    # 웹용 회원가입 로그인
    path('signuppage',signuppage,name='signuppage'),
    path('signup',signup,name='signup'),
    path('loginpage',loginpage,name='loginpage'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
]
