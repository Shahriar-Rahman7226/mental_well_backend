from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel, ClientProfileModel
from apps.schedule_management.models import CounselorSchedule
from external.choice_tuple import AppointmentCancelStatus, AppointmentStatus
from apps.user.models import UserModel


class AppointmentRequest(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_request', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_request', on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(CounselorSchedule, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=AppointmentStatus, default=AppointmentStatus[0][0])
    appointment_details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='appointment_request'
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.client.user.full_name if self.client.user else ''} - {self.status if self.status else ''}"
    

class AppointmentRequestCancel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='request_cancel_user', on_delete=models.CASCADE, blank=True, null=True)
    appointment = models.ForeignKey(AppointmentRequest, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    emergency_document = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=AppointmentCancelStatus, default=AppointmentCancelStatus[0][0])
    is_refund = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table='appointment_request_cancel'
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.user.full_name if self.user else ''} - {self.status if self.status else ''}"




