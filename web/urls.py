
from django.urls import path
from . import views
from .views import *
app_name='web'
urlpatterns = [
    path('webtest',upload_file,name='webtest'),
    #path('postcreate/',views.test,name='test')
]
