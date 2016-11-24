from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from models import *
from MiaDB.settings import docker,openStack,ansible


# Create your views here.
def GetImages(request):

    return JsonResponse({"status": "Success"})


def GetImageInfo(request,dns):

    return JsonResponse({"status": "Success"})


@csrf_exempt
def CreateImage(request):
    logging.debug("Create DataBase")
    data = json.loads(request.body)
    instanceDNS = data["dns"]

    return JsonResponse({"status": "Success"})