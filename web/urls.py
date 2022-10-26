
from django.urls import path
from .views import *
app_name='web'
urlpatterns = [
    path('test',test,name='test'),
]
