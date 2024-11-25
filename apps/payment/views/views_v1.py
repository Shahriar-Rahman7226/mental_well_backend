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
from apps.appointment_management.models import AppointmentRequestCancel

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
    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Payment instance does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if (data['paid_amount']!=instance.due_amount):
        #     return Response({'message': 'Please pay the exact due amount.'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Generate a UUID and get the first 5 characters
        unique_id = str(request.user.id)[:5]
    
        # Get the last 4 digits of the phone number
        last_4_digits = request.user.phone_number[-4:]

        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)
    
        # Construct the transaction ID
        data['transaction_id'] = f"#{unique_id}{last_4_digits}{timestamp}"

        data['platform_fee'] = float(data['paid_amount']) * 0.05
        data['final_amount'] = float(data['paid_amount']) - data['platform_fee']
        data['is_paid'] = True
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment_obj = serializer.save()
            subject = 'Mental Well'
            client_message = f'Your payment of {payment_obj.due_amount} was successful. Transaction id: {payment_obj.transaction_id}.'
            counselor_message = f'Payment of {payment_obj.final_amount} (5% deducted as platform fee) was made by client {payment_obj.client.user.full_name} on {payment_obj.payment_date}. Transaction id: {payment_obj.transaction_id}.'
            send_email(payment_obj.counselor.user.id, subject, counselor_message, None)
            send_email(None, subject, client_message, request.user.id)
            print(request.data['transaction_id'])
            return Response({'message': 'Payment updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Refund Payment",
                value={
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    @transaction.atomic()
    def payment_refund(self, request, *args, **kwargs):
        data = request.data
        instance = self.queryset.filter(id=kwargs['id']).first()
        appointment_instance = AppointmentRequestCancel.objects.filter(id=kwargs['appointment_cancellation_id'], is_refund=True).first()

        if not instance:
            return Response({'message': 'Payment instance does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not appointment_instance:
             return Response({'message': 'Appointment Cancellation instance does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        temp_amount = data['final_amount']
        data['platform_fee'] = 0
        data['final_amount'] = 0
        data['is_refund'] = True

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment_obj = serializer.save()
            subject = 'Mental Well'
            client_message = f'Your payment refund of {payment_obj.due_amount} was successful. Transaction id: {payment_obj.transaction_id}.'
            counselor_message = f'Payment refund of {temp_amount} was requested by client {payment_obj.client.user.full_name}. Transaction id: {payment_obj.transaction_id}.'
            send_email(payment_obj.counselor.user.id, subject, counselor_message, None)
            send_email(payment_obj.client.user.id, subject, client_message, None)
            print(request.data['transaction_id'])
            return Response({'message': 'Payment Refund was successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'client_id', "description": 'Filter by client_id'},
        {"name": 'is_paid', "description": 'Filter by payment status'},
        {"name": 'is_refund', "description": 'Filter by refund status'},
        {"name": 'payment_method', "description": 'Filter by payment method'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        client_id = request.query_params.get('client_id', None)
        is_paid = request.query_params.get('is_paid', None)
        is_refund = request.query_params.get('is_refund', None)
        payment_method = request.query_params.get('payment_method', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        if client_id:
            queryset = queryset.filter(client=client_id)
        if is_paid:
            queryset = queryset.filter(is_paid=is_paid)
        if is_refund:
            queryset = queryset.filter(is_refund=is_refund)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

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
            serializer = PaymentClientSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PaymentClientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Payment does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
