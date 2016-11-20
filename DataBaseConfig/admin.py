from django.contrib import admin
from models import *


# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name",)


class DataBaseAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "application",
                    "databaseImage",
                    "numberOfInstance",
                    "hostVolumePath",
                    "containerVolumePath")

    search_fields = ["name","application"]
    list_filter = ["application","databaseImage"]


admin.site.register(Application,ApplicationAdmin)
admin.site.register(DataBase,DataBaseAdmin)