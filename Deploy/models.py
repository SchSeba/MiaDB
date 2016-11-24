from __future__ import unicode_literals
from django.db import models
from DataBase.models import *


# Create your models here.
class DeployPlan(models.Model):
    name = models.CharField(max_length=120, unique=True)
    vendor = models.ForeignKey(Vendor)
    compose = models.TextField()

    def __unicode__(self):
        return self.name


class Cluster(models.Model):
    dns = models.CharField(max_length=20)
    project = models.CharField(max_length=120)
    vendor = models.ForeignKey(Vendor)
    createDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.dns

    class Meta:
        unique_together = ("dns","project")

class Node(models.Model):
    dns = models.CharField(max_length=20, unique=True)
    cluster = models.ForeignKey(Cluster)


    def __unicode__(self):
            return self.dns