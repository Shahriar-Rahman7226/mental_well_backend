from django.db import models
from abstract.base_model import CustomModel
from external.choice_tuple import PaymentMethodType
from apps.user_profile.models import CounselorProfileModel, ClientProfileModel
from apps.appointment_management.models import AppointmentRequest

# Create your models here.
class Payment(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_payment', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_payment', on_delete=models.CASCADE, blank=True, null=True)
    appointment = models.ForeignKey(AppointmentRequest, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    due_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    payment_method = models.CharField(max_length=100, choices=PaymentMethodType, default=PaymentMethodType[0][0], blank=True, null=True)
    platform_fee = models.FloatField(blank=True, null=True)  # 5% platform fee
    final_amount = models.FloatField(blank=True, null=True)
    is_paid = models.BooleanField(blank=True, null=True, default=False)
    is_refund = models.BooleanField(blank=True, null=True, default=False)
    payslip = models.FileField(blank=True, null=True) # If paid in cash

    class Meta:
        db_table = 'payment'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.user.full_name if self.client.user else ''} ({self.transaction_id if self.transaction_id else ''})"
