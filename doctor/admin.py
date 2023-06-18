from django.contrib import admin
from .models import Doctor, Timetable, Pricing
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Timetable)
admin.site.register(Pricing)