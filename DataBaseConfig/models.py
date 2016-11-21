from __future__ import unicode_literals
from django.db import models
from DockerConfig.models import *


# Create your models here.
class DataBase(models.Model):
    deploymentConfig = models.ForeignKey(DeploymentConfig)
    hostVolumePath = models.TextField()
    containerVolumePath = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("applicationName","dbName")