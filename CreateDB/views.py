from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

import json

# Create your views here.
class CreateDataBase(View):

    def post(self,request):


        JsonResponse({})