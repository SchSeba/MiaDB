from __future__ import unicode_literals
from django.db import models
from DataBaseConfig.models import *


# Create your models here.
class DockerServer(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    ip = models.CharField(max_length=15,db_index=True)
    port = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'ip',)

""" Running data """

class Deployment(models.Model):
    statusChoices = (
        ("R","Running"),
        ("S","Stopped"),
        ("W","Waiting"),
    )
    application = models.CharField(max_length=150)
    dockerServer = models.ForeignKey(DockerServer)
    status = models.CharField(max_length=10,choices=statusChoices)

    def __unicode__(self):
        return self.application

    class Meta:
        unique_together = ("application", "dockerServer")

class Container(models.Model):
    containerID = models.CharField(max_length=15)
    containerName = models.CharField(max_length=150, unique=True)
    deployment = models.ForeignKey(Deployment)
    dataBase = models.ForeignKey(DataBase)

    def __unicode__(self):
        return self.containerName

""" End Running data """

""" Deployment Configuration """
class DeploymentPlan(models.Model):
    name = models.CharField(max_length=150)
    explain = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Procedure(models.Model):
    deploymentPlan = models.ForeignKey(DeploymentPlan)
    sequence = models.IntegerField(default=1)
    deploymentConfig = models.ForeignKey(DeploymentConfig)

    def __unicode__(self):
        return self.deploymentPlan + "_" + self.sequence

    class Meta:
        unique_together = ("deploymentPlan", "sequence")

""" End Deployment Configuration """