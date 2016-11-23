from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from MiaDB.settings import docker,openStack,ansible
from models import *
import logging
import json

logger = logging.getLogger(__name__)

def GetDeployPlans(request):
    return JsonResponse({"status": "Success"})


def GetDeployPlan(request,DeploymentName):
    deployPlan = DeployPlan.objects.get(name=DeploymentName)

    return JsonResponse({"status": "Success"})


"""
DNS: Dns for the Cluster
DeploymentPlan: Name For the Deployment Plan
Vendor: DataBase Vendor(type)
Project: DataBase project owner
IP: IP addr from the vip
"""
@csrf_exempt
def Deploy(self,request):
  try:
      data = json.loads(request.body)
      logger.debug("Get DeploymentPlan " + data["DeploymentPlan"])
      deployPlan = DeployPlan.objects.get(name=data["DeploymentPlan"])
      deploySeq = DeploySequence.objects.filter(deployPlan=deployPlan).order_by("-sequence")
      instanceDNS = data["DNS"]

      newCluster = Cluster.objects.create(dns=instanceDNS+"-vip",ip=data["IP"],vendor=Vendor.objects.get(name=data["Vendor"]))
      newCluster.save()
      parameters = {"PROJECT":data["Project"]}

      for seq in deploySeq:
          logger.debug("Start Server Creation for DNS " + instanceDNS + " with image " + seq.instanceType.imageName)
          ipddr = openStack.CreateServer(instanceDNS + "-" + str(seq.sequence), seq.instanceType.imageName)
          parameters["IPADDRSEQ" + str(seq.sequence)] = ipddr
          parameters["DNSSEQ" + str(seq.sequence)] = instanceDNS + "-" + str(seq.sequence)
          parameters["SEQ"] = str(seq.sequence)

          logger.debug("End Server Creation")

          logger.debug("Start Ansible Playbook")
          playbook = seq.instanceType.ansiblePlaybook



          ansible.RunPlayBook(instanceDNS, playbook)

  except Exception as e:
      return JsonResponse({"status": "Fail",
                           "Message": e.message})


# Create your views here.
@method_decorator(csrf_exempt,name="dispatch")
class Cluster(View):
    def get(self,request,ClusterDNS):
        cluster = Cluster.objects.filter(dns=ClusterDNS)

        return JsonResponse({"status": "Success"})

