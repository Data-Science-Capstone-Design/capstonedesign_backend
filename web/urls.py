
from django.urls import path
from . import views
from .views import *
app_name='web'
urlpatterns = [
    # path('templates/html/index',upload_file,name='index'),
    path('main/',main,name='main'),
    path('upload_file/',upload_file,name='upload_file'),
    path('about/',about,name='about'),
     path('view/',view,name='view'),

    #path('postcreate/',views.test,name='test')
]
