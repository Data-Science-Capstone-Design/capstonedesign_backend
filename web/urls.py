
from django.urls import path
from . import views
from .views import *
app_name='web'
urlpatterns = [
    path('excel_save',excel_save,name='excel_save'),

    path('main/',main,name='main'),
    path('make_voucher_page/',make_voucher_page,name='make_voucher_page'),
    path('make_vouchers/',make_vouchers,name='make_vouchers'),
    path('show_vouchers/',show_vouchers,name='show_vouchers'),
    # path('templates/html/index',upload_file,name='index'),
    path('set_main_page_excel/',set_main_page_excel,name='set_main_page_excel'),
    path('register_product/',register_product,name='register_product'),
    # path('upload_file/',upload_file,name='upload_file'),
    path('about/',about,name='about'),
    path('download_excel/',download_excel,name='download_excel'),
    path('send_sms_page/<str:phone_num>/',send_sms_page,name='send_sms_page'),
    path('send_sms/',send_sms,name='send_sms'),
    path('close/',close,name='close'),
    path('show_payment_info/',show_payment_info,name='show_payment_info'),

    #path('postcreate/',views.test,name='test')

    # 웹용 회원가입 로그인
    path('signuppage/',signuppage,name='signuppage'),
    path('signup/',signup,name='signup'),
    path('loginpage/',loginpage,name='loginpage'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
]
