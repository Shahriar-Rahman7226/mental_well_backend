from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class AppointmentRequestSerializer(ModelSerializer):

    class Meta:
        model = AppointmentRequest
        exclude = exclude_list
