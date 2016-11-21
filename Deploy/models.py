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
    application = models.CharField(max_length=150, unique=True)
    dockerServer = models.ForeignKey(DockerServer)
    status = models.CharField(max_length=10,choices=statusChoices)


class Container(models.Model):
    deployment = models.ForeignKey(Deployment)
    containerName = models.CharField(max_length=150,unique=True)
    containerID = models.CharField(max_length=15)
    dataBase = models.ForeignKey(DataBase)

""" End Running data """

""" Deployment Configuration """
class DeploymentPlan(models.Model):
    name = models.CharField(max_length=150)
    explain = models.TextField(blank=True)


class Procedure(models.Model):
    deploymentPlan = models.ForeignKey(DeploymentPlan)
    sequence = models.IntegerField()
    deploymentConfig = models.ForeignKey(DeploymentConfig)

    class Meta:
        unique_together = ("deploymentPlan", "sequence")

""" End Deployment Configuration """