from rest_framework.serializers import ModelSerializer
from apps.payment.models import Payment

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        exclude = exclude_list
