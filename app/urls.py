
from django.urls import path
from .views import *
app_nampe='app'
urlpatterns = [
    path('test',test,name='test' ),
    path('signup',signup,name='signup' ),
    path('login',login,name='login' ),
    path('coupon_registration',coupon_registration,name='coupon_registration' ),
    path('get_my_cash',get_my_cash,name='get_my_cash' ),
]
