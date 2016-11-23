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
@method_decorator(csrf_exempt,name="dispatch")
class Instance(View):
    def get(self,request,dns):
        database = Instance.objects.filter(dns=dns)

        return JsonResponse({"status": "Success"})

    def post(self,request):
        logging.debug("Create DataBase")
        data = json.loads(request.body)
        instanceDNS = data["dns"]
        instanceType = InstanceType.objects.get(name=data["instanceType"])

        if Instance.objects.get(dns = instanceDNS):
            return JsonResponse({"status": "Fail",
                                 "Message": "DNS Exist"})
        else:
            if not openStack.CreateServer(instanceDNS,instanceType.imageName):
                return JsonResponse({"status": "Fail",
                                     "Message": "Fail to Create Server"})
            else:
                if not ansible.RunPlayBook(instanceDNS,instanceType.ansiblePlaybook):
                    return JsonResponse({"status": "Fail",
                                         "Message": "Fail to Run Ansible PlayBook on instance"})

            return JsonResponse({"status": "Success"})