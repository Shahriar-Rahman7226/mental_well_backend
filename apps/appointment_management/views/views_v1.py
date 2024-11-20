from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.appointment_management.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users
from apps.payment.serializers.serializers_v1 import PaymentSerializer

@extend_schema(tags=['Appointment Request'])
class AppointmentRequestViewSet(ModelViewSet):
    model_class = AppointmentRequest
    serializer_class = AppointmentRequestSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Appointment Request",
                value={
                    "counselor": "string",
                    "schedule": "string",
                    "booking_date": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=data['counselor'], user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        
        client_instance = ClientProfileModel.objects.filter(user__id=request.user.id, user__user_role='CLIENT').first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['client']=request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Appointment Request created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Appointment Request",
                value={
                    "counselor": "string",
                    "schedule": "string",
                    "booking_date": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Appointment Request updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Appointment Request Status",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['status'] == 'CONFIRMED':
            payment_instance = {
                'counselor': instance.counselor,
                'client': instance.client,
                'appointment': instance.id,
                'due_amount': instance.counselor.user.pay_per_session,
            }
            payment_serializer = PaymentSerializer(data=payment_instance)
            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            appointment_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your appointment request on {appointment_obj.schedule.day} was {appointment_obj.status}.'
            send_email(appointment_obj.client.user.id, subject, message, None)
            return Response({'message': 'Appointment Request status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_request(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id, status='CONFIRMED')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    @allowed_users(allowed_roles=['ADMIN', 'COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
