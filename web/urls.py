
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
]
