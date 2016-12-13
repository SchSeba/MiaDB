from django.contrib import admin
from models import *


# Register your models here.
class DeployPlanAdmin(admin.ModelAdmin):
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

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("serviceID","name","deployment")
    search_fields = ["name"]
    list_filter = ["deployment"]

admin.site.register(DeployPlan,DeployPlanAdmin)
admin.site.register(Swarm,SwarmAdmin)
admin.site.register(Deployment,DeploymentAdmin)
admin.site.register(SwarmCluster,SwarmClusterAdmin)
admin.site.register(Service,ServiceAdmin)