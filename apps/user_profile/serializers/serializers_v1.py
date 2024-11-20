from rest_framework import serializers
from rest_framework.serializers import *

from apps.user_profile.models import *
from apps.user.serializers.serializers_v1 import UserListSerializer

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]


class SpecializationSerializer(ModelSerializer):
    
    class Meta:
        model = SpecializationModel
        exclude = exclude_list


class CounselorProfileCreateSerializer(ModelSerializer):
    
    class Meta:
        model = CounselorProfileModel
        fields = ['user', 'certificate', 'identity_document', 'specializations', 'description', 'license_number', 'website', 'linked_in']


class CounselorProfileUpdateSerializer(ModelField):

    class Meta:
        model = CounselorProfileModel
        fields = ['status']


class CounselorProfileListSerializer(ModelField):
    user = UserListSerializer()

    class Meta:
        model = CounselorProfileModel
        exclude = exclude_list


class ClientProfileCreateSerializer(ModelSerializer):
    
    class Meta:
        model = ClientProfileModel
        fields = ['user', 'description', 'goals', 'emergency_contact']


class ClientProfileUpdateSerializer(ModelField):

    class Meta:
        model = ClientProfileModel
        fields = ['status']


class ClientProfileListSerializer(ModelField):
    user = UserListSerializer()

    class Meta:
        model = ClientProfileModel
        exclude = exclude_list

class CounselorAchievementsSerializer(ModelSerializer):

    class Meta:
        model = CounselorAchievements
        exclude = exclude_list

class FounderProfileCreateSerializer(ModelSerializer):

    class Meta:
        model = CounselorAchievements
        exclude = exclude_list

class FounderProfileListSerializer(ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = CounselorAchievements
        exclude = exclude_list