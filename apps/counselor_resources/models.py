from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import CounselorProfileModel
from external.choice_tuple import ResourceStatus, ResourceType

# Create your models here.
class CounselorResource(CustomModel):
    image = models.ImageField(upload_to='counselor_resource/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True) 
    author = models.ForeignKey(CounselorProfileModel, related_name='author_resource', on_delete=models.CASCADE, blank=True, null=True) 
    resource_file = models.FileField(blank=True, null=True)
    resource_link = models.URLField(blank=True, null=True)
    resource_type = models.CharField(max_length=100, blank=True, null=True, choices=ResourceType)
    published_at = models.DateTimeField(blank=True, null=True)  
    status = models.CharField(max_length=100, blank=True, null=True, choices=ResourceStatus, default=ResourceStatus[0][0])
    is_published = models.BooleanField(blank=True, null=True, default=False) 

    def __str__(self):
        return f"{self.title if self.title else ''} - {self.author.user.full_name if self.author.user else ''} ({self.resource_type if self.resource_type else ''})"

    class Meta:
        db_table='counselor_resource'
        ordering = ['-created_at'] 


class OtherResource(CustomModel):
    image = models.ImageField(upload_to='other_resource/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True) 
    resource_file = models.FileField(blank=True, null=True)
    resource_link = models.URLField(blank=True, null=True)
    resource_type = models.CharField(max_length=100, blank=True, null=True, choices=ResourceType)
    published_at = models.DateTimeField(blank=True, null=True)  
    is_published = models.BooleanField(blank=True, null=True, default=False) 

    def __str__(self):
        return f"{self.title if self.title else ''} - {self.resource_type if self.resource_type else ''}"

    class Meta:
        db_table='other_resource'
        ordering = ['-created_at'] 
