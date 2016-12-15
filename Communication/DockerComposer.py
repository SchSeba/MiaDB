from django.template import Template,Context
from MiaDB.settings import BasePath
import yaml


class DockerComposer():
    def Createyaml(self,composeText,params):
        composeText = composeText.replace("{{OVERLAY_NETWORK}}",params["OVERLAY_NETWORK"])\
                                 .replace("{{BasePath}}",BasePath)\
                                 .replace("{{projectName}}",params["projectName"])

        yamlData = yaml.load(composeText)

        context = Context(params)

        for index in range(yamlData["services"].__len__()):
            service = yamlData["services"][index].keys()[0]
            serviceYaml = yaml.dump(yamlData["services"][index][service])
            serviceYaml = serviceYaml.replace("{{SERVICE_COUNT}}",str(index + 1))

            serviceYaml = Template(serviceYaml)
            yamlData["services"][index][service] = yaml.load(serviceYaml.render(context))

        return yaml.dump(yamlData)

    def GetDockerServicesCommand(self,yamlText):
        yamlData = yaml.load(yamlText)
        dockerServicesCommand = []

        for index in range(yamlData["services"].__len__()):
            service = yamlData["services"][index].keys()[0]
            serviceYaml = yamlData["services"][index][service]

            if yamlData.has_key("network"):
                serviceYaml["networks"] = [yamlData["network"]]
            else:
                serviceYaml["networks"] = []

            if not serviceYaml.has_key("mounts"):
                serviceYaml["mounts"] = []

            if not serviceYaml.has_key("env"):
                serviceYaml["env"] = []

            if not serviceYaml.has_key("mode"):
                serviceYaml["mode"] = None

            if not serviceYaml.has_key("publish"):
                serviceYaml["publish"] = {}
            else:
                publishDict = {}
                for publish in serviceYaml["publish"]:
                    publishDict[int(publish.split(":")[0])] = int(publish.split(":")[1])
                serviceYaml["publish"] = publishDict

            dockerServicesCommand.append(serviceYaml)

        return dockerServicesCommand


    def CreateServiceCommand(self,composeText,params):
        yamlText = self.Createyaml(composeText,params)

        # Create services command
        dockerServicesCommand = self.GetDockerServicesCommand(yamlText)

        return dockerServicesCommand, yamlText
