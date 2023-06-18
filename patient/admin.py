from django.contrib import admin
from .models import Patient, Record, Request, Appointment, Prescription, Medication

admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(Request)
admin.site.register(Appointment)
admin.site.register(Medication)
admin.site.register(Prescription)
# admin.site.register(Complaint)
