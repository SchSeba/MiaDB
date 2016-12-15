from Deploy.models import *
from DockerConnector import *

class DockerService():
    def __init__(self,deployment):
        self.deployment = deployment
        swarmCluster = SwarmCluster.objects.get(name=deployment.swarm)
        swarmServers = Swarm.objects.filter(swarmCluster=swarmCluster)

        swarmManagers = []
        for manager in swarmServers:
            swarmManagers.append(manager.ip + ":" + str(manager.port))

        self.dockerConnector = DockerConnector(swarmManagers)


    def RemoveServices(self):
        for service in Service.objects.filter(deployment=self.deployment):
            self.dockerConnector.RemoveService(service.serviceID)