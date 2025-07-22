from django.contrib import admin
from .models import SensorReading, DailySummary

admin.site.register(SensorReading)
admin.site.register(DailySummary)
