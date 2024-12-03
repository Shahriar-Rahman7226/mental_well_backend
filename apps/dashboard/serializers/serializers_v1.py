from rest_framework.serializers import *
from ..models import *
from apps.user_profile.models import FounderProfileModel
from apps.user_profile.serializers.serializers_v1 import FounderProfileListSerializer

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
    founders = SerializerMethodField()

    class Meta:
        model = AboutUs
        exclude = exclude_list

    def get_founders(self, obj):
        founders = FounderProfileModel.objects.all()
        return FounderProfileListSerializer(founders, many=True).data


class FooterSerializer(ModelSerializer):
    
    class Meta:
        model = FooterModel
        exclude = exclude_list
