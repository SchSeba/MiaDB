from django.contrib import admin
from models import *


# Register your models here.
class DataBaseAdmin(admin.ModelAdmin):
    list_display = ("applicationName",
                    "dbName",
                    "deploymentConfig",
                    "hostVolumePath",
                    "containerVolumePath")

    search_fields = ["applicationName"]
    list_filter = ["applicationName","deploymentConfig"]


admin.site.register(DataBase,DataBaseAdmin)