from django.template import Template,Context
from MiaDB.settings import BasePath
import yaml
from docker import Client
from docker.types import TaskTemplate, ContainerSpec

class DockerComposer():
    def Createyaml(self,composeText,params):
        composeText.replace("{{OVERLAY_NETWORK}}",params["OVERLAY_NETWORK"])\
                   .replace("{{BasePath}}",BasePath)\
                   .replace("{{projectName}}",params["projectName"])

        yamlData = yaml.load(composeText)

        context = Context(params)

        for index in range(yamlData["services"].__len__()):
            service = yamlData["services"][index].keys()[0]
            serviceYaml = yaml.dump(yamlData["services"][index][service])
            serviceYaml = serviceYaml.replace("{{SERVICE_COUNT}}",str(index + 1))

            serviceYaml = Template(serviceYaml)
            yamlData["services"][index][service]  = yaml.load(serviceYaml.render(context))


        return yaml.dump(yamlData)

    def GetDockerServicesCommand(self,yamlText):
        yamlData = yaml.load(yamlText)
        dockerServicesCommand = []

        for index in range(yamlData["services"].__len__()):
            service = yamlData["services"][index].keys()[0]
            serviceYaml = yamlData["services"][index][service]
            mounts = []

            #For bind mounts
            if serviceYaml.has_key("mount"):
                for mountKeys in serviceYaml["mount"]["bind"].keys():
                    serviceYaml["mount"]["bind"][mountKeys]["type"]="bind"
                    mounts.append(serviceYaml["mount"]["bind"][mountKeys])

            cont = ContainerSpec(serviceYaml["image"],env=serviceYaml["env"],mounts=mounts)
            task_tmpl = TaskTemplate(cont)

            dockerServicesCommand.append({"name":serviceYaml["name"],
                                          "service":task_tmpl})

        return dockerServicesCommand


    def CreateServiceCommand(self,composeText,params):
        yamlText = self.Createyaml(composeText,params)

        #Create services command
        dockerServicesCommand = self.GetDockerServicesCommand(yamlText)


        return dockerServicesCommand, yamlText