
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenBlacklistView,TokenRefreshView,TokenVerifyView,TokenObtainPairView

app_nampe='app'
urlpatterns = [
    #post
    path('signup',signup,name='signup' ),
    path('login',TokenObtainPairView.as_view(),name="login"),
    # {"refresh": 토큰} 꼴로 post
    path('logout',TokenBlacklistView.as_view(),name="logout"),

    #access토큰 재발급, {"refresh": 토큰} 꼴로 post
    path('token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    #토큰 유효성 검사, {"token": 토큰} 꼴로 post, refresh access 둘다 검사가능
    path('token-verify', TokenVerifyView.as_view(), name='token_verify'),
   
    path('coupon_registration',coupon_registration,name='coupon_registration' ),
    path('get_my_cash',get_my_cash,name='get_my_cash' ),
]
