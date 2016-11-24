from __future__ import unicode_literals
from django.db import models


# Create your models here.
class InstanceType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    imageName = models.CharField(max_length=120)
    explain = models.TextField(blank=True)
    ansiblePlaybook = models.TextField()

    def __unicode__(self):
        return self.name


class ConfigType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    explain = models.TextField(blank=True)
    instanceType = models.ForeignKey(InstanceType)
    ansiblePlaybook = models.TextField()

    def __unicode__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __unicode__(self):
        return self.name