from django.db import models
from apps.user.models import UserModel
from abstract.base_model import CustomModel
from apps.user_profile.models import *
from external.choice_tuple import ResourceType


class BannerModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='banner/', blank=True, null=True)

    def __str__(self):
        return f"{self.title if self.title else ''}"
    
    class Meta:
        db_table='banner_model'
        ordering=['-created_at']


class MotivationModel(CustomModel):
    quote_text = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.quote_text if self.quote_text else ''} - {self.author if self.author else ''}"
    
    class Meta:
        db_table='motivation_model'
        ordering=['-created_at']





class LegalDocument(CustomModel):
    details = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    licence_document = models.FileField(blank=True, null=True)

    class Meta:
        db_table='legal_document'
        ordering=['-created_at']


class PrivacyPolicy(CustomModel):
    details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='privacy_policy'
        ordering=['-created_at']


class AboutUs(CustomModel):
    introduction = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        db_table='about_us'
        ordering=['-created_at']


class FooterModel(CustomModel):
    image = models.ImageField(upload_to='footer/', blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_support = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        db_table='footer_models'
        ordering=['-created_at']
