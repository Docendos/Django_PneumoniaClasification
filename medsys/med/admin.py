from django.contrib import admin

from med.models import Doctor, Patient, Appointment, Image

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Image)
