from Deploy.models import *
from DockerConnector import *

import logging
import os
import shutil

logger = logging.getLogger("MiaDB")

class DockerService():
    def __init__(self,deployment):
        self.deployment = deployment
        swarmCluster = SwarmCluster.objects.get(name=deployment.swarm)
        swarmServers = Swarm.objects.filter(swarmCluster=swarmCluster)

        swarmManagers = []
        for manager in swarmServers:
            swarmManagers.append(manager.ip + ":" + str(manager.port))

        self.dockerConnector = DockerConnector(swarmManagers)


    def CreateService(self,dockerServicesCommand):
        logger.info("Creating services")
        serviceIDs = []
        for service in dockerServicesCommand:

            logger.debug("Create Folder and file on docker host if not exist")
            for mount in service["mounts"]:
                # Check for file or directory
                if mount["source"][-1] == "/":
                    if os.path.exists(mount["source"]):
                        shutil.rmtree(mount["source"])
                    os.makedirs(mount["source"])
                else:
                    open(mount["source"], "w").close()


            logger.debug("Create service name " + service["name"])
            service = self.dockerConnector.CreateService(service)
            serviceIDs.append(service.id)
            logger.debug("Create successfully Service ID " + service.id)
            Service.objects.create(deployment=self.deployment,
                                   serviceID=service.id,
                                   name=service.name)

        return serviceIDs


    def RemoveServices(self):
        for service in Service.objects.filter(deployment=self.deployment):
            self.dockerConnector.RemoveService(service.serviceID)