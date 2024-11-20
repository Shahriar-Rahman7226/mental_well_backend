from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class CounselorScheduleSerializer(ModelSerializer):

    class Meta:
        model = CounselorSchedule
        exclude = exclude_list
