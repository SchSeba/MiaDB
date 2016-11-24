from __future__ import unicode_literals
from django.db import models
from DataBase.models import *

# Create your models here.
class DeployPlan(models.Model):
    name = models.CharField(max_length=120, unique=True)
    vendor = models.ForeignKey(Vendor)

    def __unicode__(self):
        return self.name

class DeploySequence(models.Model):
    deployPlan = models.ForeignKey(DeployPlan)
    sequence = models.IntegerField(default=1)
    instanceType = models.ForeignKey(InstanceType)

    def __unicode__(self):
        return self.deployPlan.name + "_" + str(self.sequence)

    class Meta:
        unique_together = ("deployPlan","sequence")


class Cluster(models.Model):
    dns = models.CharField(max_length=20)
    project = models.CharField(max_length=120)
    ip = models.CharField(max_length=15)
    vendor = models.ForeignKey(Vendor)
    createDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.dns

    class Meta:
        unique_together = ("dns","project")

class Node(models.Model):
    dns = models.CharField(max_length=20, unique=True)
    ip = models.CharField(max_length=15)
    cluster = models.ForeignKey(Cluster)
    instanceType = models.ForeignKey(InstanceType)

    def __unicode__(self):
            return self.dns