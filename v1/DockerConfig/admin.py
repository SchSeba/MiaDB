from django.contrib import admin
from .models import *


# Register your models here.
class EnvironmentVariableAdmin(admin.ModelAdmin):
    list_display = ("variableName","variableValue")
    search_fields = ["variableName"]


class DeploymentConfigAdmin(admin.ModelAdmin):
    list_display = ("name","dataBaseImageName")
    search_fields = ["name","dataBaseImageName"]
    list_filter = ["dataBaseImageName"]


admin.site.register(EnvironmentVariable,EnvironmentVariableAdmin)
admin.site.register(DeploymentConfig,DeploymentConfigAdmin)
