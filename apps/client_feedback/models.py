from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel, ClientProfileModel
from django.core.validators import MinValueValidator, MaxValueValidator

# Client Feedback
class Review(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_review', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_review', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    review_text = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True, default=False) 
    appointment_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    is_anonymous = models.BooleanField(blank=True, null=True, default=False)
    counselor_name = models.CharField(max_length=100, blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.client_name if self.client_name else ''} - {self.rating if self.rating else ''}"

    class Meta:
        db_table = 'review'
        ordering = ['-created_at'] 


class FAQModel(CustomModel):
    client = models.ForeignKey(ClientProfileModel, related_name='faq_client', on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    asnwer = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f"{self.client.user.full_name if self.client.user else ''} - {self.rating if self.rating else ''}"
    
    class Meta:
        db_table='faq_model'
        ordering=['-created_at']
