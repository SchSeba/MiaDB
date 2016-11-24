from django.contrib import admin
from models import *


# Register your models here.
class DeployPlanAdmin(admin.ModelAdmin):
    list_display = ("name","vendor")
    search_fields = ["name","vendor"]
    list_filter = ["vendor"]

class DeploySequenceAdmin(admin.ModelAdmin):
    list_display = ("deployPlan","sequence","instanceType")
    list_filter = ["deployPlan","instanceType"]

class ClusterAdmin(admin.ModelAdmin):
    list_display = ("dns","vendor","createDate")
    search_fields = ["dns","vendor"]
    list_filter = ["vendor"]

class NodeAdmin(admin.ModelAdmin):
    list_display = ("dns","cluster")
    search_fields = ["dns"]
    list_filter = ["cluster"]


admin.site.register(DeployPlan,DeployPlanAdmin)
admin.site.register(Cluster,ClusterAdmin)
admin.site.register(Node,NodeAdmin)