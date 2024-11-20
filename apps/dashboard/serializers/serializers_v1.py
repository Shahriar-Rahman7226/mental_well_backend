from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class BannerSerializer(ModelSerializer):
    
    class Meta:
        model = BannerModel
        exclude = exclude_list


class MotivationSerializer(ModelSerializer):
    
    class Meta:
        model = MotivationModel
        exclude = exclude_list


class LegalDocumentSerializer(ModelSerializer):
    
    class Meta:
        model = LegalDocument
        exclude = exclude_list


class PrivacyPolicySerializer(ModelSerializer):
    
    class Meta:
        model = PrivacyPolicy
        exclude = exclude_list


class AboutUsSerializer(ModelSerializer):
    
    class Meta:
        model = AboutUs
        exclude = exclude_list


class FooterSerializer(ModelSerializer):
    
    class Meta:
        model = FooterModel
        exclude = exclude_list
