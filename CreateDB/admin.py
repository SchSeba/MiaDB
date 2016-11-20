from django.contrib import admin
from models import *


# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name",)


class DataBaseImageAdmin(admin.ModelAdmin):
    list_display = ("name", "explain",)
    search_fields = ["name"]


class DataBaseAdmin(admin.ModelAdmin):
    list_display = ("name", "application","databaseImage","numberOfInstanse")
    search_fields = ["name"]
    list_filter = ["application"]

admin.site.register(Application,ApplicationAdmin)
admin.site.register(DataBase,DataBaseAdmin)
admin.site.register(DataBaseImage,DataBaseImageAdmin)