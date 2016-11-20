from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)


    def __unicode__(self):
        return self.name


class DataBaseImage(models.Model):
    name = models.CharField(max_length=150,unique=True, db_index=True)
    explain = models.TextField()

    def __unicode__(self):
        return self.name


class DataBase(models.Model):
    name = models.CharField(max_length=100,unique=True)
    application = models.ForeignKey(Application)
    databaseImage = models.ForeignKey(DataBaseImage)
    numberOfInstanse = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name
