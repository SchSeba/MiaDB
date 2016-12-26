import docker
import os
import shutil
from docker.types import IPAMConfig
from docker.types import EndpointSpec
from MiaDB.settings import BasePath

class DockerConnector():

    def __init__(self,dockerManagerList):
        isManagerAlive = False
        for manager in dockerManagerList:
            try:
                self.dockerClient = docker.DockerClient(base_url="tcp://" + manager)
                self.dockerClient.info()
                isManagerAlive = True
                break

            except Exception as e:
                pass

        if not isManagerAlive:
            raise Exception("Not manager server alive found")


    def CreateService(self, ServiceParam):

        # Check if the network exist
        if self.dockerClient.networks.list(names=ServiceParam["networks"]).__len__() == 0:
            ipam_config = docker.types.IPAMConfig()
            self.dockerClient.networks.create(name=ServiceParam["networks"][0], driver="overlay",
                                              ipam=ipam_config)

        service = self.dockerClient.services.create(image=ServiceParam["image"],
                                                      mounts=ServiceParam["mounts"],
                                                      env=ServiceParam["env"],
                                                      name=ServiceParam["name"],
                                                      networks=ServiceParam["networks"],
                                                      mode=ServiceParam["mode"],
                                                      endpoint_spec=EndpointSpec(ports=ServiceParam["publish"]))

        return service


    def StopService(self,serviceId):
        if self.dockerClient.services.list(filters={'id': serviceId}).__len__() == 1:
            service = self.dockerClient.services.get(serviceId)

            service.remove()


    def RemoveService(self,serviceId):
        if self.dockerClient.services.list(filters={'id': serviceId}).__len__() == 1:
            service = self.dockerClient.services.get(serviceId)
            self.DeleteStorage(service)
            service.remove()


    def DeleteStorage(self,service):
        if service.attrs[u'Spec'][u'TaskTemplate'][u'ContainerSpec'].has_key('Mounts'):
            for mount in service.attrs[u'Spec'][u'TaskTemplate'][u'ContainerSpec'][u'Mounts']:
                if os.path.exists(mount["Source"]):
                    if mount["Source"][-1] == "/":
                        shutil.rmtree(mount["Source"])
                    else:
                        os.remove(mount["Source"])
