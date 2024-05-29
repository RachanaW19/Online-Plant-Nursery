from django.contrib import admin
from .models import Plant

# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display=['id','name','pdetails','cat','is_active']
    list_filter=['cat','is_active']

admin.site.register(Plant,PlantAdmin)