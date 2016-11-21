from __future__ import unicode_literals
from django.db import models


# Create your models here.
class EnvironmentVariable(models.Model):
    variableName = models.CharField(max_length=120)
    variableValue = models.TextField()

    def __unicode__(self):
        return self.variableName

    class Meta:
        unique_together = ('variableName', 'variableValue',)


class DeploymentConfig(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    dataBaseImageName = models.CharField(max_length=150)
    environmentVariable = models.ManyToManyField(EnvironmentVariable)

    def __unicode__(self):
        return self.name
