from django.contrib import admin
from .models import *


# Register your models here.
class DataBaseImageAdmin(admin.ModelAdmin):
    list_display = ("name", "explain",)
    search_fields = ["name"]


class EnvironmentVariableAdmin(admin.ModelAdmin):
    list_display = ("DataBaseImage","variableName","variableValue")
    search_fields = ["DataBaseImage"]


class DeploymentConfigAdmin(admin.ModelAdmin):
    list_display = ("name","dataBaseImage")
    search_fields = ["name","dataBaseImage"]
    list_filter = ["dataBaseImage"]


admin.site.register(DataBaseImage,DataBaseImageAdmin)
admin.site.register(EnvironmentVariable,EnvironmentVariableAdmin)
admin.site.register(DeploymentConfig,DeploymentConfigAdmin)
