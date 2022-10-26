
from django.urls import path
from .views import *
app_nampe='app'
urlpatterns = [
    path('test',test,name='test' ),
]
