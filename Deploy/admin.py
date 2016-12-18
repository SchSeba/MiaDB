from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms

from Communication.DockerComposer import DockerComposer
from Communication.DockerService import DockerService
from models import *

class DeployPlanForm(forms.ModelForm):
    class Meta:
        model=DeployPlan
        fields = '__all__'

    def clean(self):
        dockerComposer = DockerComposer()

        try:
            dockerComposer.CreateServiceCommand(self.cleaned_data.get("compose"), {"params": {}})
        except Exception as e:
            raise ValidationError("Error Validating the compose text\n Error: " + e.message)


# Register your models here.
class DeployPlanAdmin(admin.ModelAdmin):
    form = DeployPlanForm
    list_display = ("name","compose")
    search_fields = ["name"]

class SwarmAdmin(admin.ModelAdmin):
    list_display = ("swarmCluster","name","ip","port")
    search_fields = ["swarmCluster","name","ip"]
    list_filter = ["swarmCluster"]

class SwarmClusterAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]

class DeploymentAdmin(admin.ModelAdmin):
    list_display = ("projectName","deployPlan","swarm","createDate")
    search_fields = ["projectName","deployPlan"]
    list_filter = ["deployPlan","swarm"]
    actions = ["delete_selected"]

    def delete_model(self, request, obj):
        dockerService = DockerService(obj)
        dockerService.RemoveServices()

        super(DeploymentAdmin, self).delete_model(request, obj)

    def delete_selected(self, request, queryset):
        for deployment in queryset:
            dockerService = DockerService(deployment)
            dockerService.RemoveServices()
            deployment.delete()


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("serviceID","name","deployment")
    search_fields = ["name"]
    list_filter = ["deployment"]

    def delete_model(self, request, obj):
        pass

admin.site.register(DeployPlan,DeployPlanAdmin)
admin.site.register(Swarm,SwarmAdmin)
admin.site.register(Deployment,DeploymentAdmin)
admin.site.register(SwarmCluster,SwarmClusterAdmin)
admin.site.register(Service,ServiceAdmin)