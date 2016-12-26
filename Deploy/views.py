from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Communication.DockerConnector import *
from Communication.DockerComposer import *
from Communication.DockerService import *
from models import *
from Scale.ScaleManager import *

import logging
import json

logger = logging.getLogger("MiaDB")


def GetDeployPlans(request):
    return JsonResponse(list(DeployPlan.objects.values("pk","name").all()),safe=False)


def GetDeployPlanByName(request,DeployPlanName):
    return JsonResponse(list(DeployPlan.objects.values().filter(name=DeployPlanName)),safe=False)


def GetDeployments(request):
    return JsonResponse(list(Deployment.objects.all().values("id",
                                                             "projectName",
                                                             "createDate",
                                                             "deployPlan__name")),safe=False)


def GetDeploymentByName(request,DeploymentByName):
    deployment = Deployment.objects.filter(projectName=DeploymentByName)[0]

    services = Service.objects.values("name", "serviceID").filter(deployment=deployment)
    deployment = Deployment.objects.values("id",
                                           "projectName",
                                           "createDate",
                                           "deployPlan__name").filter(projectName=DeploymentByName)[0]
    deployment["services"] = list(services)
    return JsonResponse(deployment, safe=False)


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

                logger.info("Start Deploy DeploymentPlan " + data["deployPlan"] + " for project " + data["projectName"] +
                            "on " + swarmCluster.name + " Swarm Cluster")

                logger.debug("Compose Request")
                dockerComposer = DockerComposer()


                dockerServicesCommand, yamlText = dockerComposer.CreateServiceCommand(deployPlan.compose,data)

                logger.debug("Create new row on database for deployment")
                deployment = Deployment.objects.create(projectName=data["projectName"],
                                                       deployPlan=deployPlan,
                                                       swarm=swarmCluster,
                                                       renderCompose=yamlText)

                logger.debug("Compose file after render \n" + deployment.renderCompose)

                try:
                    dockerService = DockerService(deployment)
                    serviceIDs = dockerService.CreateService(dockerServicesCommand)

                    return JsonResponse({"status": "SUCCESS",
                                         "Message": serviceIDs})

                except Exception as e:
                    deployment.delete()
                    logger.error(str(e))
                    return JsonResponse({"status": "Fail",
                                         "Message": str(e.message)})

        except Exception as e:
            logger.error(e.message)
            return JsonResponse({"status": "Fail",
                               "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})


"""
projectName: Dns for the Cluster
deployPlan: Name For the Deployment Plan
swarmCluster: name of swarm cluster
"""
@csrf_exempt
def StartDeployment(request):
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
                                           deployPlan=DeployPlan.objects.get(name=data["deployPlan"])).__len__() == 0:
                raise Exception("Project Doesnt exist")

            else:
                logger.debug("Get DeploymentPlan " + data["deployPlan"])
                deployPlan = DeployPlan.objects.get(name=data["deployPlan"])
                swarmCluster = SwarmCluster.objects.get(name=data["swarmCluster"])

                deployment = Deployment.objects.get(projectName=data["projectName"],
                                                       deployPlan=deployPlan,
                                                       swarm=swarmCluster)

                try:
                    logger.debug("Compose Request")
                    dockerComposer = DockerComposer()

                    dockerServicesCommand = dockerComposer.GetDockerServicesCommand(deployment.renderCompose)

                    dockerService = DockerService(deployment)
                    serviceIDs = dockerService.StartService(dockerServicesCommand)

                    return JsonResponse({"status": "SUCCESS",
                                         "Message": serviceIDs})

                except Exception as e:
                    deployment.delete()
                    logger.error(str(e.message))
                    return JsonResponse({"status": "Fail",
                                         "Message": str(e.message)})

        except Exception as e:
            logger.error(e.message)
            return JsonResponse({"status": "Fail",
                               "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})


"""
projectName: Dns for the Cluster
deployPlan: Name For the Deployment Plan
swarmCluster: name of swarm cluster
"""
@csrf_exempt
def StopDeployment(request):
    if request.method == "POST":
        try:
            logger.info("Load json data")
            data = json.loads(request.body)
            logger.debug(data)

            deployment = Deployment.objects.filter(projectName=data["projectName"],
                                                  swarm=SwarmCluster.objects.get(name=data["swarmCluster"]),
                                                  deployPlan=DeployPlan.objects.get(name=data["deployPlan"]))

            if deployment.__len__() != 1:
                raise Exception("Project Doesnt exist")
            else:
                deployment = deployment[0]
                deploymentName = deployment.projectName
                dockerService = DockerService(deployment)
                dockerService.StopServices()

                return JsonResponse({"status": "SUCCESS",
                                 "Message": "Success Stop " + deploymentName + " Deployment"})

        except Exception as e:
            logger.error(e.message)
            return JsonResponse({"status": "Fail",
                                 "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})


"""
projectName: Dns for the Cluster
deployPlan: Name For the Deployment Plan
swarmCluster: name of swarm cluster
params: directory of parameters
"""
@csrf_exempt
def RemoveDeployment(request):
    if request.method == "POST":
        try:
            logger.info("Load json data")
            data = json.loads(request.body)
            logger.debug(data)

            deployment = Deployment.objects.filter(projectName=data["projectName"],
                                                  swarm=SwarmCluster.objects.get(name=data["swarmCluster"]),
                                                  deployPlan=DeployPlan.objects.get(name=data["deployPlan"]))

            if deployment.__len__() != 1:
                raise Exception("Project Doesnt exist")
            else:
                deployment = deployment[0]
                deploymentName = deployment.projectName
                dockerService = DockerService(deployment)
                dockerService.RemoveServices()

                deployment.delete()

            return JsonResponse({"status": "SUCCESS",
                                 "Message": "Success Remove " + deploymentName + " Deployment"})

        except Exception as e:
            logger.error(e.message)
            return JsonResponse({"status": "Fail",
                                 "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})

"""
projectName: Dns for the Cluster
deployPlan: Name For the Deployment Plan
swarmCluster: name of swarm cluster
params: directory of parameters
"""
#TODO: Not finnish
@csrf_exempt
def ScaleUP(request):
    if request.method == "POST":
        try:
            logger.info("Load json data")
            data = json.loads(request.body)
            logger.debug(data)

            deployment = Deployment.objects.filter(projectName=data["projectName"],
                                         swarm=SwarmCluster.objects.get(name=data["swarmCluster"]),
                                         deployPlan=DeployPlan.objects.get(name=data["deployPlan"]))

            if deployment.__len__() == 0:
                raise Exception("Project Doesnt exist")
            else:
                scaleManager = ScaleManager(deployment[0])
                scaleManager.ScaleUp()

        except Exception as e:
            logger.error(e.message)
            return JsonResponse({"status": "Fail",
                                 "Message": e.message})
    else:
        return JsonResponse({"status": "Fail",
                             "Message": "Send only with POST"})