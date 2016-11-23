from django.contrib import admin
from .models import *


# Register your models here.
class DockerServerAdmin(admin.ModelAdmin):
    list_display = ("name","ip","port",)
    search_fields = ["name","ip"]


class DeploymentAdmin(admin.ModelAdmin):
    list_display = ("application","dockerServer","status")
    search_fields = ["dockerServer"]
    list_filter = ["dockerServer","status"]


class ContainerAdmin(admin.ModelAdmin):
    list_display = ("containerID", "containerName", "deployment","dataBase")
    search_fields = ["containerName","containerID"]
    list_filter = ["dataBase"]


class DeploymentPlanAdmin(admin.ModelAdmin):
    list_display = ("name","explain")
    search_fields = ("name")


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("deploymentPlan","sequence","deploymentConfig")
    search_fields = ["deploymentPlan"]


admin.site.register(DockerServer,DockerServerAdmin)
admin.site.register(Deployment,DeploymentAdmin)
admin.site.register(Container,ContainerAdmin)
admin.site.register(DeploymentPlan,DeploymentPlanAdmin)
