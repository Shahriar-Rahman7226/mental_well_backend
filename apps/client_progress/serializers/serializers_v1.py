from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class ClientProgressSerializer(ModelSerializer):

    class Meta:
        model = ClientProgress
        exclude = exclude_list

class ClientProgressDetailsSerializer(ModelSerializer):

    class Meta:
        model = ClientProgressDetails
        exclude = exclude_list
