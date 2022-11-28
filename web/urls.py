
from django.urls import path
from . import views
from .views import *
app_name='web'
urlpatterns = [
    # path('templates/html/index',upload_file,name='index'),
    path('main/',main,name='main'),

    #path('postcreate/',views.test,name='test')
]
