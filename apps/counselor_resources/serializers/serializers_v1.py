from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class CounselorResourceSerializer(ModelSerializer):

    class Meta:
        model = CounselorResource
        exclude = exclude_list

class OtherResourcesSerializer(ModelSerializer):
    
    class Meta:
        model = OtherResource
        exclude = exclude_list
