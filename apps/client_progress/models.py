from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel, ClientProfileModel
from apps.appointment_management.models import AppointmentRequest
from external.choice_tuple import ProgressStatus

# Create your models here.
class ClientProgress(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='client_progress_counselor', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_progress_client', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ProgressStatus, default=ProgressStatus[0][0])
    session_count = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.client.user.full_name if self.client.user else ''} - {self.status if self.status else ''}"
    
    class Meta:
        db_table='client_progress'
        ordering=['-created_at']


class ClientProgressDetails(CustomModel):
    progress = models.ForeignKey(ClientProfileModel, related_name='progress_details', on_delete=models.CASCADE, blank=True, null=True)
    appointment = models.ForeignKey(AppointmentRequest, related_name='progress_appointment', on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    progress_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return f"{self.progress.client.user.full_name if self.progress.client.user else ''} - {self.progress_date if self.progress_date else ''} ({self.progress.session_count if self.progress else ''})"
    
    class Meta:
        db_table='client_progress_details'
        ordering=['-created_at']
