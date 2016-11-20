from __future__ import unicode_literals
from django.db import models


# Create your models here.
class DataBaseImage(models.Model):
    name = models.CharField(max_length=150,unique=True, db_index=True)
    explain = models.TextField()

    def __unicode__(self):
        return self.name


class EnvironmentVariable(models.Model):
    DataBaseImage = models.ForeignKey(DataBaseImage)
    variableName = models.CharField(max_length=120)
    variableValue = models.TextField()

    def __unicode__(self):
        return self.variableName

    class Meta:
        unique_together = ('DataBaseImage', 'variableName',)


class DeploymentConfig(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    dataBaseImage = models.ForeignKey(DataBaseImage)
    config = models.TextField()

    def __unicode__(self):
        return self.name
