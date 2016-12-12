from docker import Client
import logging

class DockerConnector():

    def __init__(self,dockerManagerList):
        isManagerAlive = False
        for manager in dockerManagerList:
            try:
                self.dockerClient = Client(base_url="tcp://" + manager)
                self.dockerClient.info()
                isManagerAlive = True
                break

            except Exception as e:
                pass

        if not isManagerAlive:
            raise Exception("Not manager server alive found")



    def CreateContainer(self,name,image,hostVolume,containerVolume,environmentVariable):
        try:
            container = self.dockerClient.create_container(
                image=image,environment=environmentVariable, volumes=[hostVolume],
                host_config=self.dockerClient.create_host_config(binds={
                    containerVolume: {
                        'bind': hostVolume,
                        'mode': 'rw',
                    }
                })
            )

            return container

        except Exception as e:
            logging.ERROR("Fail to Create Container Exception Message: " + e.message)
            return {"status":"Fail",
                    "Message": e.message}


    def RemoveContainer(self,containerID):
        try:
            self.dockerClient.remove_container(container=containerID)
            return {"status": "Success"}

        except Exception as e:
            logging.ERROR("Fail to Remove Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def StartContainer(self,containerID):
        try:
            response = self.dockerClient.start(container=containerID)
            return {"status": "Success",
                    "Message": response}

        except Exception as e:
            logging.ERROR("Fail to Start Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def StopContainer(self,containerID):
        try:
            response = self.dockerClient.stop(container=containerID)
            return {"status": "Success",
                    "Message": response}

        except Exception as e:
            logging.ERROR("Fail to Stop Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def InspectContainer(self,containerID):
        try:
            response = self.dockerClient.inspect_container(container=containerID)
            return {"status": "Success",
                    "Data": response}

        except Exception as e:
            logging.ERROR("Fail to Inspect Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def Kill(self,containerID):
        try:
            self.dockerClient.kill(container=containerID)
            return {"status": "Success"}

        except Exception as e:
            logging.ERROR("Fail to Inspect Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def Logs(self,containerID):
        try:
            response = self.dockerClient.logs(container=containerID)
            return {"status": "Success",
                    "Message": response}

        except Exception as e:
            logging.ERROR("Fail to Inspect Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def RunContainer(self,name,image,hostVolume,containerVolume):
        try:
            container = self.CreateContainer(name, image, hostVolume, containerVolume)
            containerID = container.get('Id')
            response = self.StartContainer(containerID)

            return {"status": "Success",
                    "Message": response,
                    "Inspect": self.InspectContainer(containerID),
                    "Logs": self.Logs(containerID)}

        except Exception as e:
            logging.ERROR("Fail to Run Container Exception Message: " + e.message)
            return {"status": "Fail",
                    "Message": e.message}


    def CreateService(self,ServiceParam):

        return self.dockerClient.create_service(ServiceParam["Service"], name=ServiceParam["name"])



