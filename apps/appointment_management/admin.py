from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AppointmentRequest)
admin.site.register(AppointmentRequestCancel)