from __future__ import unicode_literals
from django.db import models
# from DataBase.models import *


# Create your models here.
class SwarmCluster(models.Model):
    name = models.CharField(max_length=120, db_index=True)

    def __unicode__(self):
        return self.name


class Swarm(models.Model):
    swarmCluster = models.ForeignKey(SwarmCluster)
    name = models.CharField(max_length=120, db_index=True)
    ip = models.CharField(max_length=15,db_index=True)
    port = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'ip',)


class DeployPlan(models.Model):
    name = models.CharField(max_length=120, unique=True)
    compose = models.TextField()

    def __unicode__(self):
        return self.name


class Deployment(models.Model):
    projectName = models.CharField(max_length=120,unique=True)
    deployPlan = models.ForeignKey(DeployPlan)
    swarm = models.ForeignKey(SwarmCluster)
    createDate = models.DateTimeField(auto_now=True)
    renderCompose = models.TextField(blank=True,default="")

    def __unicode__(self):
        return self.projectName

    class Meta:
        unique_together=("projectName","deployPlan","swarm")


class Service(models.Model):
    deployment = models.ForeignKey(Deployment)
    serviceID = models.CharField(max_length=15)
    name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name