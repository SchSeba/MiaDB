from django.contrib import admin
from models import *

# Register your models here.
class InstanceTypeAdmin(admin.ModelAdmin):
    list_display = ("name","imageName","ansiblePlaybook","explain")
    search_fields = ["name","imageName"]


class ConfigTypeAdmin(admin.ModelAdmin):
    list_display = ("name","instanceType","ansiblePlaybook","explain")
    search_fields = ["name","ansiblePlaybook"]
    list_filter = ["instanceType","ansiblePlaybook"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]

admin.site.register(InstanceType,InstanceTypeAdmin)
admin.site.register(ConfigType,ConfigTypeAdmin)
admin.site.register(Vendor,VendorAdmin)