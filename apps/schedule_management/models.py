from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel
from external.choice_tuple import ScheduleStatus, Days


class CounselorSchedule(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_schedule', on_delete=models.CASCADE, blank=True, null=True)
    day = models.CharField(max_length=100, blank=True, null=True, choices=Days)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    # is_available = models.BooleanField(blank=True, null=True, default=False)
    is_booked = models.BooleanField(blank=True, null=True, default=False)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ScheduleStatus, default=ScheduleStatus[0][0])

    class Meta:
        db_table='counselor_schedule'
        ordering=['-created_at']

    def __str__(self):
        return f"{self.day if self.day else ''} ({self.start_time if self.start_time else ''} to {self.end_time if self.end_time else ''})"
