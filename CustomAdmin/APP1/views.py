import json
from django.http.request import HttpHeaders
from django.shortcuts import render
from firebase_admin.messaging import *

from django.http import HttpResponse
import requests
import json

from APP1.models import *
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from APP1.forms import *
from django.shortcuts import render
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django import forms
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered




def index(request):
 
    return render(request, 'index.html')