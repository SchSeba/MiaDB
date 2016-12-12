from django.shortcuts import render
from django.template import Template, Context
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Communication.DockerConnector import *
from Communication.DockerComposer import *
from models import *

import logging
import json
import yaml

logger = logging.getLogger(__name__)

def GetDeployPlans(request):
    return JsonResponse({"status": "Success"})


def GetDeployPlan(request,DeploymentName):
    deployPlan = DeployPlan.objects.get(name=DeploymentName)

    return JsonResponse({"status": "Success"})


"""
projectName: Dns for the Cluster
deployPlan: Name For the Deployment Plan
swarmCluster: name of swarm cluster
params: directory of parameters
"""
@csrf_exempt
def Deploy(request):
    if request.method == "POST":
        try:
            logger.info("Load json data")
            data = json.loads(request.body)
            logger.debug(data)

            if SwarmCluster.objects.filter(name=data["swarmCluster"]).__len__() == 0:
                raise Exception("Swarm Cluster doesnt exist")

            elif DeployPlan.objects.filter(name=data["deployPlan"]).__len__() == 0:
                raise Exception("DeployPlan doesnt exist")

            elif Deployment.objects.filter(projectName=data["projectName"],
                                           swarm=SwarmCluster.objects.get(name=data["swarmCluster"]),
                                           deployPlan=DeployPlan.objects.get(name=data["deployPlan"])).__len__() != 0:
                raise Exception("Project Already exist")

            else:
                logger.debug("Get DeploymentPlan " + data["deployPlan"])
                deployPlan = DeployPlan.objects.get(name=data["deployPlan"])
                swarmCluster = SwarmCluster.objects.get(name=data["swarmCluster"])
                swarmServers = Swarm.objects.filter(swarmCluster=swarmCluster)

                logger.info("Start Deploy DeploymentPlan " + data["deployPlan"] + " for project " + data["projectName"] +
                            "on " + swarmCluster.name + " Swarm Cluster")

                logger.debug("Create new row on database for deployment")
                # deployment = Deployment.objects.create(projectName=data["projectName"],
                #                                        deployPlan=deployPlan,
                #                                        swarm=swarmCluster)


                logger.debug("Compose Request")
                dockerComposer = DockerComposer()

                params = data["params"]
                params["projectName"] = data["projectName"]
                params["OVERLAY_NETWORK"] = "Net_" + data["projectName"]

                dockerServicesCommand, yamlText = dockerComposer.CreateServiceCommand(deployPlan.compose,params)
                # logger.debug("Compose file after render \n" + deployment.renderCompose)

                swarmManagers = []
                for manager in swarmServers:
                    swarmManagers.append(manager.ip + ":" + manager.port)
                dockerConnector = DockerConnector(swarmCluster)

                for service in dockerServicesCommand:
                    serviceID = dockerConnector.CreateService(service)


        except Exception as e:
            return JsonResponse({"status": "Fail",
                               "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})
