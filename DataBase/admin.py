from django.contrib import admin
from models import *

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name","imageName","dokerFile","vendor")
    search_fields = ["name","imageName"]

class VendorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]

admin.site.register(Image,ImageAdmin)
admin.site.register(Vendor,VendorAdmin)