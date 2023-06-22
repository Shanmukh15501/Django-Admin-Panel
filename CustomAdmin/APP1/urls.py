from django.contrib import admin
from django.urls import path
from django.urls import path,include
from APP1.views import *

urlpatterns = [

        path('' , index),
]

