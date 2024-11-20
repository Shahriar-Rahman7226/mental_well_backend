from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.payment.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email
from rest_framework import status
from external.permission_decorator import allowed_users
import time

@extend_schema(tags=['Payment'])
class PaymentViewSet(ModelViewSet):
    model_class = Payment
    serializer_class = PaymentSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Payment",
                value={
                    "paid_amount": "string",
                    "payment_method": "string",
                    "payment_date": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['CLIENT'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Payment instance does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Get the last 4 digits of the phone number
        last_4_digits = request.user.phone_number[-4:]
    
        # Generate a UUID and get the first 5 characters
        unique_id = request.user.id[:5]
    
        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)
    
        # Construct the transaction ID
        request.data['transaction_id'] = f"#{last_4_digits}{unique_id}{timestamp}"

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your payment of {payment_obj.due_amount} was successful.'
            send_email(None, subject, message, request.user.id)
            print(request.data['transaction_id'])
            return Response({'message': 'Payment updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'client_id', "description": 'Filter by client_id'},

    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        client_id = request.query_params.get('client_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        elif client_id:
            queryset = queryset.filter(client=client_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'client_id', "description": 'Filter by client_id'},

    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_counselor_payment_history(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id)
        client_id = request.query_params.get('client_id', None)
        if client_id:
            queryset = queryset.filter(client=client_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['CLIENT'])
    def get_client_payment_history(self, request, *args, **kwargs):
        queryset = self.queryset.filter(client=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Payment does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
