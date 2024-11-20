from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel, ClientProfileModel
from apps.schedule_management.models import CounselorSchedule
from external.choice_tuple import AppointmentStatus


class AppointmentRequest(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_request', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_request', on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(CounselorSchedule, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    status= models.CharField(max_length=100, blank=True, null=True, choices=AppointmentStatus, default=AppointmentStatus[0][0])

    class Meta:
        db_table='appointment_request'
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.client.user.full_name if self.client.user else ''} - {self.status if self.status else ''}"




