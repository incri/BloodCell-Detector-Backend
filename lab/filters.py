from django_filters.rest_framework import FilterSet
from . import models

class BloodTestFilter(FilterSet):
    class Meta:
        model = models.BloodTest
        fields = {
            'patient_id' : ['exact'],
            'created_at' : ['lt', 'gt'],
            'title': ['exact'],
            'detection_status' : ['exact']
        }