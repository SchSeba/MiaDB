from django.contrib import admin
from .models import *


# Register your models here.
class DockerServerAdmin(admin.ModelAdmin):
    list_display = ("name","ip","port",)
    search_fields = ["name","ip"]


class DeploymentAdmin(admin.ModelAdmin):
    list_display = ("dockerServer","dataBase","numberOfInstance","status")
    search_fields = ["dockerServer","dataBase","status"]
    list_filter = ["dockerServer","status"]


class ContainerAdmin(admin.ModelAdmin):
    list_display = ("containerID", "name", "deployment")
    search_fields = ["name"]
    list_filter = ["deployment"]


admin.site.register(DockerServer,DockerServerAdmin)
admin.site.register(Deployment,DeploymentAdmin)
admin.site.register(Container,ContainerAdmin)