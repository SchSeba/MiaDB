from __future__ import unicode_literals
from django.db import models
from DockerConfig.models import *


# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class DataBase(models.Model):
    name = models.CharField(max_length=100,unique=True)
    application = models.ForeignKey(Application)
    databaseImage = models.ForeignKey(DataBaseImage)
    numberOfInstance = models.IntegerField(default=1)
    hostVolumePath = models.TextField()
    containerVolumePath = models.TextField()

    def __unicode__(self):
        return self.name
