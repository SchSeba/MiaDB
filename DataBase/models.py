from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=120, unique=True)
    imageName = models.CharField(max_length=120)
    dokerFile = models.TextField()
    vendor = models.ForeignKey(Vendor)

    def __unicode__(self):
        return self.name