from django.contrib import admin
from . import models

@admin.register(models.BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']
    list_per_page = 10

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'birth_date']
    list_per_page = 10

class DetectionAdmin(admin.ModelAdmin):
    list_display = ['started_at', 'detection_status']
    list_editable = ['detection_status']
    list_per_page = 10

admin.site.register(models.Address)
admin.site.register(models.Detection)