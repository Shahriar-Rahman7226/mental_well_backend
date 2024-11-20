from rest_framework.serializers import *
from ..models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class FAQSerializer(ModelSerializer):

    class Meta:
        model = FAQModel
        exclude = exclude_list



class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        exclude = exclude_list
