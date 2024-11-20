from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel
from external.choice_tuple import ScheduleStatus, Days

# Create your models here.
# Available time slots or schedules for each counselor
class CounselorSchedule(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_schedule', on_delete=models.CASCADE, blank=True, null=True)
    day = models.CharField(max_length=100, blank=True, null=True, choices=Days)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(blank=True, null=True, default=True)
    is_booked = models.BooleanField(blank=True, null=True, default=False)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ScheduleStatus, default=ScheduleStatus[0][0])

    class Meta:
        db_table='counselor_schedule'
        ordering=['-created_at']

    def __str__(self):
        return f"{self.counselor.user.full_name if self.counselor.user else ''} - {self.day if self.day else ''}"
