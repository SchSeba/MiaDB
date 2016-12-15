from Deploy.models import *
from Communication.DockerConnector import *

import importlib


class ScaleManager:
    def __init__(self, deployment):
        self.deployment = deployment

    def ScaleUp(self):
        try:
            DeployPlanScale = importlib.import_module('Scale.DeployPlanScale.postgres')
            scale = DeployPlanScale.ScaleUP()
            scale.UP()
        except Exception as e:
            pass

    def ScaleDown(self):
        pass